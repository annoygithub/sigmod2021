/*******************************************************************\

Module: Solver Factory

Author: Daniel Kroening, Peter Schrammel

\*******************************************************************/

/// \file
/// Solver Factory

#ifndef CPROVER_GOTO_CHECKER_SOLVER_FACTORY_H
#define CPROVER_GOTO_CHECKER_SOLVER_FACTORY_H

#include <memory>

#include <solvers/smt2/smt2_dec.h>

class message_handlert;
class namespacet;
class optionst;
class propt;
class decision_proceduret;
class stack_decision_proceduret;

class solver_factoryt
{
public:
  /// Note: The solver returned will hold a reference to the namespace `ns`.
  solver_factoryt(
    const optionst &_options,
    const namespacet &_ns,
    message_handlert &_message_handler,
    bool _output_xml_in_refinement);

  // The solver class,
  // which owns a variety of allocated objects.
  class solvert
  {
  public:
    solvert() = default;
    explicit solvert(std::unique_ptr<decision_proceduret> p);
    solvert(std::unique_ptr<decision_proceduret> p1, std::unique_ptr<propt> p2);
    solvert(
      std::unique_ptr<decision_proceduret> p1,
      std::unique_ptr<std::ofstream> p2);

    decision_proceduret &decision_procedure() const;
    stack_decision_proceduret &stack_decision_procedure() const;
    propt &prop() const;

    void set_decision_procedure(std::unique_ptr<decision_proceduret> p);
    void set_prop(std::unique_ptr<propt> p);
    void set_ofstream(std::unique_ptr<std::ofstream> p);

    // the objects are deleted in the opposite order they appear below
    std::unique_ptr<std::ofstream> ofstream_ptr;
    std::unique_ptr<propt> prop_ptr;
    std::unique_ptr<decision_proceduret> decision_procedure_ptr;
  };

  /// Returns a solvert object
  virtual std::unique_ptr<solvert> get_solver();

  virtual ~solver_factoryt() = default;

protected:
  const optionst &options;
  const namespacet &ns;
  message_handlert &message_handler;
  const bool output_xml_in_refinement;

  std::unique_ptr<solvert> get_default();
  std::unique_ptr<solvert> get_dimacs();
  std::unique_ptr<solvert> get_bv_refinement();
  std::unique_ptr<solvert> get_string_refinement();
  std::unique_ptr<solvert> get_smt2(smt2_dect::solvert solver);

  smt2_dect::solvert get_smt2_solver_type() const;

  /// Sets the timeout of \p decision_procedure if the `solver-time-limit`
  /// option has a positive value (in seconds).
  /// \note Most solvers silently ignore the time limit at the moment.
  void
  set_decision_procedure_time_limit(decision_proceduret &decision_procedure);

  // consistency checks during solver creation
  void no_beautification();
  void no_incremental_check();
};

#endif // CPROVER_GOTO_CHECKER_SOLVER_FACTORY_H
