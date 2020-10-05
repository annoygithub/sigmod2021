// function_check_02

// This test checks the use of quantifiers in ensures clauses.
// A known bug (resolved in PR #2278) causes the use of quantifiers
// in ensures to fail.

int initialize(int *arr)
  __CPROVER_ensures(
    __CPROVER_forall {int i; (0 <= i && i < 10) ==> arr[i] == i}
  )
{
  for(int i = 0; i < 10; i++)
  {
    arr[i] = i;
  }

  return 0;
}

int main()
{
  int arr[10];
  initialize(arr);
}
