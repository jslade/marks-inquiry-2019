import optparse

from .settings import Settings


class ArgParser(object):
    def __init__(self):
        self.parser = optparse.OptionParser()

        self.parser.add_option('--playground', dest='playground', default=False,
                               action='store_true',
                               help='Run in playground mode')


    def set_opts(self, opts):
        Settings.playground = opts.playground


    def parse(self, args):
        opts, args = self.parser.parse_args(args)
        self.set_opts(opts)
        return(opts, args)
