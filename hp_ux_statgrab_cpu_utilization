#!/usr/local/bin/bash
# modified by 4815162342lost
#plugin for monitoring CPU Utilization on HP-UX
#changes: plugin output not save to file, only variable
#memory monitoring removed

export PATH=$PATH:/usr/sbin:/usr/bin:/usr/contrib/bin:/usr/local/bin/
export LD_LIBRARY_PATH=/usr/local/lib/
if which statgrab > /dev/null ; then
    if statgrab_output=`statgrab cpu. 2>/dev/null`
        then
            echo "<<<statgrab_cpu>>>"
            echo "$statgrab_output" | grep "^cpu\." | cut -d. -f2-99 | sed 's/ *= */ /'
    fi
fi
