#include <cmath>
#include <cstdint>
#include <cstdio>
#include <utility>
uint32_t perceptualDuty(uint32_t pct, uint32_t full) {
  if (pct == 0) return 0;
  if (pct > 100) pct = 100;
  // Built once per resolution: apply() runs on every slider step and fade tick.
  static uint32_t tableFull = 0;
  static uint16_t table[101] = {};
  if (tableFull != full) {
    uint32_t duty = 0;
    for (uint32_t p = 1; p <= 100; ++p) {
      const auto ideal = static_cast<uint32_t>(std::lround(std::pow(static_cast<double>(full), (p - 1) / 99.0)));
      duty = ideal > duty ? ideal : duty + 1u;
      table[p] = static_cast<uint16_t>(duty < full ? duty : full);
    }
    tableFull = full;
  }
  return table[pct];
}
std::pair<uint32_t,uint32_t> channels(uint32_t totalDuty, uint32_t _warmPercent) {
  bool dual=true;
  uint32_t warmDuty = 0;
  uint32_t coolDuty = totalDuty;
  if (dual) {
    warmDuty = (totalDuty * _warmPercent + 50u) / 100u;
    coolDuty = totalDuty - warmDuty;
  }
  return {coolDuty,warmDuty};
}
struct Light { float rampFromDutyF=0, rampToDutyF=5, ditherAcc=0; int64_t rampUs=1000000; };
uint32_t sample(Light& light, int64_t t) {
  const float k = static_cast<float>(t) / static_cast<float>(light.rampUs);
  const float s0 = sqrtf(light.rampFromDutyF);
  const float s1 = sqrtf(light.rampToDutyF);
  const float sNow = s0 + (s1 - s0) * k;
  const float dutyF = sNow * sNow;
  auto duty = static_cast<uint32_t>(dutyF);
  light.ditherAcc += dutyF - static_cast<float>(duty);
  if (light.ditherAcc >= 1.0f) {
    light.ditherAcc -= 1.0f;
    ++duty;
  }

  return duty;
}
int main() {
  puts("steady: brightness_pct warmth_pct total cold warm warm_fraction");
  for(unsigned w: {50u,30u}) for(unsigned p: {1u,2u,3u,4u,5u,6u,7u,8u,9u,10u}) {
    auto d=perceptualDuty(p,2047); auto [c,h]=channels(d,w);
    printf("%u %u %u %u %u %.6f\n",p,w,d,c,h,h/double(d));
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
  for(unsigned b=0;b<5;b++) printf("[%u,%u): samples=%u mean_cold=%.6f mean_warm=%.6f warm_fraction=%.6f lit_warm_only=%u\n",b,b+1,counts[b],cold[b]/double(counts[b]),warm[b]/double(counts[b]),warm[b]/double(cold[b]+warm[b]),coldOff[b]);
}
