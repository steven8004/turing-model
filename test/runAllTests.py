import sys
sys.path.append("..")

import glob
from os.path import dirname, basename, join

from turing_models.utilities.error import TuringError
from turing_models.utilities.turing_date import setDateFormatType, TuringDateFormatTypes
setDateFormatType(TuringDateFormatTypes.UK_LONG)

# I put this here to get the library loaded and header printed before loop
from TuringTestCases import TuringTestCases

print("Looking in folder:", dirname(__file__))
modules = sorted(glob.glob(join(dirname(__file__), "Test*.py")))
numModules = len(modules)

''' This is the index of the file - change this to start later in the list '''
n = 0
m = numModules

###############################################################################

for moduleFileName in modules[n:m+1]:

    try:

        moduleTextName = basename(moduleFileName[:-3])    
        print("TEST: %3d out of %3d: MODULE: %-35s "% (n+1, numModules,
                                                       moduleTextName), end="")
        moduleName = __import__(moduleTextName)    
        numErrors = moduleName.testCases._globalNumErrors
        numWarnings = moduleName.testCases._globalNumWarnings
    
        print("WARNINGS: %3d   ERRORS: %3d " % (numWarnings, numErrors), end ="")
    
        if numErrors > 0:
            for i in range(0, numErrors):
                print("*", end="")
        
        print("")    
        n = n + 1

    # Want testing to continue even if a module has an exception
    except TuringError as err:
        print("TuringError:", err._message, "************")
        n = n + 1
        pass
    except ValueError as err:
        print("Value Error:", err.args[0], "************")
        n = n + 1
        pass
    except NameError as err:
        print("Name Error:", err.args[0], "************")
        n = n + 1
        pass
    except TypeError as err:
        print("Type Error:", err.args[0], "************")
        n = n + 1
        pass
    except BaseException as e:
        print("Base error:", e)
        n = n + 1
        pass
    except:
        print("Unexpected error:", sys.exc_info()[0])
        n = n + 1
        pass
        
###############################################################################    
