from pathlib import Path
import hashlib, subprocess
base=Path('/Users/kryvusha/Xteink')
firm=base/'firmware'
out=base/'qa_runs/frontlight-colour-2026-11-06'
sdk=(firm/'freeink-sdk/libs/hardware/FrontlightManager/src/FrontlightManager.cpp').read_text()
hal=(firm/'lib/hal/HalFrontlight.cpp').read_text()
curve=sdk[sdk.index('uint32_t perceptualDuty(uint32_t pct, uint32_t full) {'):sdk.index('\n#else', sdk.index('uint32_t perceptualDuty(uint32_t pct, uint32_t full) {'))]
split=sdk[sdk.index('  uint32_t warmDuty = 0;'):sdk.index('\n#ifdef FREEINK_FRONTLIGHT_LS',sdk.index('  uint32_t warmDuty = 0;'))]
fade=hal[hal.index('  const float k = static_cast<float>(t)'):hal.index('  light.manager.setTotalDuty(duty);')]
program='''#include <cmath>
#include <cstdint>
#include <cstdio>
#include <utility>
'''+curve+'''
std::pair<uint32_t,uint32_t> channels(uint32_t totalDuty, uint32_t _warmPercent) {
  bool dual=true;
'''+split+'''
  return {coolDuty,warmDuty};
}
struct Light { float rampFromDutyF=0, rampToDutyF=5, ditherAcc=0; int64_t rampUs=1000000; };
uint32_t sample(Light& light, int64_t t) {
'''+fade+'''
  return duty;
}
int main() {
  puts("steady: brightness_pct warmth_pct total cold warm warm_fraction");
  for(unsigned w: {50u,30u}) for(unsigned p: {1u,2u,3u,4u,5u,6u,7u,8u,9u,10u}) {
    auto d=perceptualDuty(p,2047); auto [c,h]=channels(d,w);
    printf("%u %u %u %u %u %.6f\\n",p,w,d,c,h,h/double(d));
  }
  puts("fade 0 -> 5%, 1000ms, warmth 50%; buckets of requested fractional total duty");
  Light l;
  unsigned counts[5]={}, cold[5]={}, warm[5]={}, coldOff[5]={};
  for(int64_t t=250;t<l.rampUs;t+=250) {
    double target=5.0*double(t)*double(t)/double(l.rampUs)/double(l.rampUs);
    unsigned b=static_cast<unsigned>(target); if(b>4) b=4;
    auto d=sample(l,t); auto [c,h]=channels(d,50);
    counts[b]++;cold[b]+=c;warm[b]+=h;if(c==0&&h>0)coldOff[b]++;
  }
  for(unsigned b=0;b<5;b++) printf("[%u,%u): samples=%u mean_cold=%.6f mean_warm=%.6f warm_fraction=%.6f lit_warm_only=%u\\n",b,b+1,counts[b],cold[b]/double(counts[b]),warm[b]/double(counts[b]),warm[b]/double(cold[b]+warm[b]),coldOff[b]);
}
'''
(out/'probe.cpp').write_text(program)
(out/'source-digests.txt').write_text('\n'.join(f'{name} {hashlib.sha256(text.encode()).hexdigest()}' for name,text in [('sdk',sdk),('hal',hal)])+'\n')
subprocess.run(['c++','-std=c++17',str(out/'probe.cpp'),'-o',str(out/'probe')],check=True)
r=subprocess.run([str(out/'probe')],text=True,capture_output=True,check=True)
(out/'result.txt').write_text(r.stdout)
print(r.stdout)
