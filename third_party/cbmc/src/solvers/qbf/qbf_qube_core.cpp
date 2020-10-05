/*******************************************************************\

Module:

Author: CM Wintersteiger

\*******************************************************************/

#include "qbf_qube_core.h"

#include <cstdlib>
#include <cstring>
#include <fstream>

#include <util/arith_tools.h>
#include <util/invariant.h>

qbf_qube_coret::qbf_qube_coret(message_handlert &message_handler)
  : qdimacs_coret(message_handler)
{
  break_lines=false;
  qbf_tmp_file="qube.qdimacs";
}

qbf_qube_coret::~qbf_qube_coret()
{
}

const std::string qbf_qube_coret::solver_text()
{
  return "QuBE w/ toplevel assignments";
}

propt::resultt qbf_qube_coret::prop_solve()
{
  if(no_clauses()==0)
    return resultt::P_SATISFIABLE;

  {
    log.status() << "QuBE: " << no_variables() << " variables, " << no_clauses()
                 << " clauses" << messaget::eom;
  }

  std::string result_tmp_file="qube.out";

  {
    std::ofstream out(qbf_tmp_file.c_str());

    // write it
    break_lines=false;
    write_qdimacs_cnf(out);
  }

  std::string options;

  // solve it
  int res=system((
    "QuBE "+options+" "+qbf_tmp_file+" > "+result_tmp_file).c_str());
  CHECK_RETURN(0==res);

  bool result=false;

  // read result
  {
    std::ifstream in(result_tmp_file.c_str());

    bool result_found=false;
    while(in)
    {
      std::string line;

      std::getline(in, line);

      if(!line.empty() && line[line.size() - 1] == '\r')
        line.resize(line.size()-1);

      if(line[0]=='V')
      {
        mp_integer b(line.substr(2).c_str());
        if(b<0)
          assignment[numeric_cast_v<std::size_t>(b.negate())] = false;
        else
          assignment[numeric_cast_v<std::size_t>(b)] = true;
      }
      else if(line=="s cnf 1")
      {
        result=true;
        result_found=true;
        break;
      }
      else if(line=="s cnf 0")
      {
        result=false;
        result_found=true;
        break;
      }
    }

    if(!result_found)
    {
      log.error() << "QuBE failed: unknown result" << messaget::eom;
      return resultt::P_ERROR;
    }
  }

  int remove_result=remove(result_tmp_file.c_str());
  if(remove_result!=0)
  {
    log.error() << "Remove failed: " << std::strerror(errno) << messaget::eom;
    return resultt::P_ERROR;
  }

  remove_result=remove(qbf_tmp_file.c_str());
  if(remove_result!=0)
  {
    log.error() << "Remove failed: " << std::strerror(errno) << messaget::eom;
    return resultt::P_ERROR;
  }

  if(result)
  {
    log.status() << "QuBE: TRUE" << messaget::eom;
    return resultt::P_SATISFIABLE;
  }
  else
  {
    log.status() << "QuBE: FALSE" << messaget::eom;
    return resultt::P_UNSATISFIABLE;
  }
}

bool qbf_qube_coret::is_in_core(literalt) const
{
  UNIMPLEMENTED;
}

qdimacs_coret::modeltypet qbf_qube_coret::m_get(literalt) const
{
  UNIMPLEMENTED;
}
