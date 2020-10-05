/*******************************************************************\

Module:

Author: CM Wintersteiger

\*******************************************************************/

#include "qbf_qube.h"

#include <cstdlib>
#include <fstream>

#include <util/invariant.h>

qbf_qubet::qbf_qubet(message_handlert &message_handler)
  : qdimacs_cnft(message_handler)
{
  // skizzo crashes on broken lines
  break_lines=false;
}

qbf_qubet::~qbf_qubet()
{
}

tvt qbf_qubet::l_get(literalt) const
{
  UNREACHABLE;
}

const std::string qbf_qubet::solver_text()
{
  return "QuBE";
}

propt::resultt qbf_qubet::prop_solve()
{
  // sKizzo crashes on empty instances
  if(no_clauses()==0)
    return resultt::P_SATISFIABLE;

  {
    log.status() << "QuBE: " << no_variables() << " variables, " << no_clauses()
                 << " clauses" << messaget::eom;
  }

  std::string qbf_tmp_file="qube.qdimacs";
  std::string result_tmp_file="qube.out";

  {
    std::ofstream out(qbf_tmp_file.c_str());

    // write it
    write_qdimacs_cnf(out);
  }

  std::string options;

  // solve it
  int res=system(
    ("QuBE "+qbf_tmp_file+options+" > "+result_tmp_file).c_str());
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

      if(line=="s cnf 0")
      {
        result=true;
        result_found=true;
        break;
      }
      else if(line=="s cnf 1")
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

  return resultt::P_ERROR;
}
