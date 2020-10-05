#include <assert.h>

struct S
{
  int i;
  char *j;
};

void touches_parameter(
  int *param,
  int *const_param,
  struct S *struct_param,
  int non_pointer_param);

int main(void)
{
  int parameter = 10;
  int unchanged_parameter = 10;
  struct S my_struct = {.i = 10, .j = "10"};
  touches_parameter(&parameter, &unchanged_parameter, &my_struct, 4);
  assert(parameter == 10);
  assert(unchanged_parameter == 10);
  assert(my_struct.i == 10);
  assert(my_struct.j == "10");

  parameter = 10;
  unchanged_parameter = 10;
  my_struct.i = 10;
  my_struct.j = "10";
  touches_parameter(&parameter, &unchanged_parameter, &my_struct, 4);
  assert(parameter == 10);
  assert(unchanged_parameter == 10);
  assert(my_struct.i == 10);
  assert(my_struct.j == "10");
}
