/*******************************************************************\

Module:

Author: Daniel Kroening, kroening@kroening.com

\*******************************************************************/

#include "qbf_skizzo.h"

#include <cstdlib>
#include <fstream>

#include <util/invariant.h>

qbf_skizzot::qbf_skizzot(message_handlert &message_handler)
  : qdimacs_cnft(message_handler)
{
  // skizzo crashes on broken lines
  break_lines=false;
}

qbf_skizzot::~qbf_skizzot()
{
}

tvt qbf_skizzot::l_get(literalt) const
{
  UNREACHABLE;
}

const std::string qbf_skizzot::solver_text()
{
  return "Skizzo";
}

propt::resultt qbf_skizzot::prop_solve()
{
  // sKizzo crashes on empty instances
  if(no_clauses()==0)
    return resultt::P_SATISFIABLE;

  {
    log.status() << "Skizzo: " << no_variables() << " variables, "
                 << no_clauses() << " clauses" << messaget::eom;
  }

  std::string qbf_tmp_file="sKizzo.qdimacs";
  std::string result_tmp_file="sKizzo.out";

  {
    std::ofstream out(qbf_tmp_file.c_str());

    // write it
    write_qdimacs_cnf(out);
  }

  std::string options;

  // solve it
  int res=system((
    "sKizzo "+qbf_tmp_file+options+" > "+result_tmp_file).c_str());
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

      if(line=="The instance evaluates to TRUE.")
      {
        result=true;
        result_found=true;
        break;
      }
      else if(line=="The instance evaluates to FALSE.")
      {
        result=false;
        result_found=true;
        break;
      }
    }

    if(!result_found)
    {
      log.error() << "Skizzo failed: unknown result" << messaget::eom;
      return resultt::P_ERROR;
    }
  }

  if(result)
  {
    log.status() << "Skizzo: TRUE" << messaget::eom;
    return resultt::P_SATISFIABLE;
  }
  else
  {
    log.status() << "Skizzo: FALSE" << messaget::eom;
    return resultt::P_UNSATISFIABLE;
  }

  return resultt::P_ERROR;
}
