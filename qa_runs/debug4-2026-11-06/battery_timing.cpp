#include <cassert>
#include <cstdint>
#include <string>
static uint32_t clockMs=1;
static bool pin=false;
static int writes=0;
static std::string event;
uint32_t millis(){return clockMs;}
struct Battery { bool isCharging()const{return pin;} };
Battery battery(){return {};}
namespace batterylog {
constexpr uint32_t TICK_MS = 20UL * 60UL * 1000UL;
constexpr uint32_t CHARGE_MIN_MS =
    10UL * 1000UL;  // a STAT pin flickering at end of charge writes at most this often
uint32_t lastTickMs = 0;
int lastCharging = -1;

bool write(const char* name,bool& charging){charging=pin;++writes;event=name;return true;}
void record(const char* event) {
  bool charging = false;
  if (write(event, charging)) {
    lastCharging = charging ? 1 : 0;
    lastTickMs = millis();
  }
}

void tick() {
  const uint32_t now = millis();
  const bool due = lastTickMs == 0 || now - lastTickMs >= TICK_MS;
  // The charge pin is a plain GPIO read: cheap to check every pass.
  const int charging = battery().isCharging() ? 1 : 0;
  if (due) {
    record("tick");
  } else if (lastCharging >= 0 && charging != lastCharging && now - lastTickMs >= CHARGE_MIN_MS) {
    record("charge");
  }
}
}
int main(){
using namespace batterylog;
record("boot"); assert(writes==1);
clockMs=60001; tick(); assert(writes==1);
clockMs=1200000; tick(); assert(writes==1);
clockMs=1200001; tick(); assert(writes==2 && event=="tick");
pin=true; clockMs+=9999; tick(); assert(writes==2);
++clockMs; tick(); assert(writes==3 && event=="charge");
clockMs+=1199999;tick();assert(writes==3);
++clockMs;tick();assert(writes==4 && event=="tick");
clockMs=UINT32_MAX-1000;record("boot");int n=writes;
clockMs=100;tick();assert(writes==n);
clockMs=1198999;tick();assert(writes==n+1);
}
