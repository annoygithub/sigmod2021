/*******************************************************************\

Module: Value Set (Flow Insensitive)

Author: Daniel Kroening, kroening@kroening.com
        CM Wintersteiger

\*******************************************************************/

/// \file
/// Value Set (Flow Insensitive)

#ifndef CPROVER_POINTER_ANALYSIS_VALUE_SET_DOMAIN_FI_H
#define CPROVER_POINTER_ANALYSIS_VALUE_SET_DOMAIN_FI_H

#include <analyses/flow_insensitive_analysis.h>

#include "value_set_fi.h"

class value_set_domain_fit:public flow_insensitive_abstract_domain_baset
{
public:
  value_set_fit value_set;

  // overloading

//  virtual bool merge(const value_set_domain_fit &other)
//  {
//    return value_set.make_union(other.value_set);
//  }

  void output(const namespacet &ns, std::ostream &out) const override
  {
    value_set.output(ns, out);
  }

  void initialize(const namespacet &) override
  {
    value_set.clear();
  }

  bool transform(
    const namespacet &ns,
    const irep_idt &function_from,
    locationt from_l,
    const irep_idt &function_to,
    locationt to_l) override;

  void get_reference_set(
    const namespacet &ns,
    const exprt &expr,
    expr_sett &expr_set) override
  {
    value_set.get_reference_set(expr, expr_set, ns);
  }

  void clear(void) override
  {
    value_set.clear();
  }
};

#endif // CPROVER_POINTER_ANALYSIS_VALUE_SET_DOMAIN_FI_H
