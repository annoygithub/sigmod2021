#include <assert.h>
#include <math.h>

int main()
{
  __CPROVER_islessgreaterd();
  assert(0);
  return 0;
}
