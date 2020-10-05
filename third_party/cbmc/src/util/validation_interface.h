/*******************************************************************\

Module: Goto program validation common command line options

Author: Daniel Poetzl

\*******************************************************************/

#ifndef CPROVER_UTIL_VALIDATION_INTERFACE_H
#define CPROVER_UTIL_VALIDATION_INTERFACE_H

#define OPT_VALIDATE                                                           \
  "(validate-goto-model)"                                                      \
  "(validate-ssa-equation)"

#define HELP_VALIDATE                                                          \
  " --validate-goto-model        enable additional well-formedness checks on " \
  "the\n"                                                                      \
  "                              goto program\n"                               \
  " --validate-ssa-equation      enable additional well-formedness checks on " \
  "the\n"                                                                      \
  "                              SSA representation\n"

#endif /* CPROVER_UTIL_VALIDATION_INTERFACE_H */
