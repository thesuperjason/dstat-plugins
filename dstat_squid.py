# Dstat plugin for measuring various squid statistics.
# Author: Jason Friedland <thesuperjason@gmail.com>
#
# Dstat is a versatile replacement for vmstat, iostat, netstat,
# nfsstat and ifstat. Dstat overcomes some of their limitations
# and adds some extra features, more counters and flexibility.
# Dstat is handy for monitoring systems during performance
# tuning tests, benchmarks or troubleshooting.
#
# See: http://dag.wieers.com/home-made/dstat/ for details
#
# This plugin has been tested with:
# - Dstat 0.6.7
# - CentOS release 5.4 (Final)
# - Python 2.4.3
# - Squid 2.6 and 2.7

global squidclient_options
squidclient_options = os.getenv('DSTAT_SQUID_OPTS') # -p 8080

class dstat_squid(dstat):
    def __init__(self):
        self.name = 'squid status'
        self.format = ('s', 8, 100)
        self.vars = ('Number of file desc currently in use', 
            'CPU Usage, 5 minute avg', 
            'Total accounted', 
            'Number of clients accessing cache',
            'Mean Object Size')
        self.nick = ('fdesc',
            'cpu5',
            'mem',
            'clients',
            'objsize')
        self.init(self.vars, 1)
        
    def check(self):
        if not os.access('/usr/sbin/squidclient', os.X_OK):
            raise Exception, 'Needs squidclient binary'
        return True

    def extract(self):
        try:
            for line in os.popen('/usr/sbin/squidclient %s mgr:info' % (squidclient_options), 'r').readlines():
                l = line.split(':')
                for item in self.vars:
                    if l[0].strip() == item:
                        self.val[item] = l[1].strip()
                        break
        except Exception, e:
            if op.debug > 1: print '%s: exception' (self.filename, e)
            for name in self.vars: self.val[name] = -1


# :TODO: Add parsing for hit ratios (splitting on ':' needs some work) - JF
#
# hit_req:
# Request Hit Ratios:	5min: 53.5%, 60min: 53.5%
# hit_byte:
# Byte Hit Ratios:	5min: 28.0%, 60min: 22.3%
#
# req_mem:
# Request Memory Hit Ratios:	5min: 2.4%, 60min: 2.4%
# req_disk:
# Request Disk Hit Ratios:	5min: 19.5%, 60min: 25.7%
