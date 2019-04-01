import optparse

from .settings import Settings


class ArgParser(object):
    def __init__(self):
        self.parser = optparse.OptionParser()

        self.parser.add_option('--playground', dest='playground', default=False,
                               action='store_true',
                               help='Run in playground mode')

        self.parser.add_option('--width', dest='width', default=1200,
                               help='Screen width')
        self.parser.add_option('--height', dest='height', default=800,
                               help='Screen height')


    def set_opts(self, opts):
        Settings.playground = opts.playground
        Settings.screen_width = int(opts.width)
        Settings.screen_height = int(opts.height)


    def parse(self, args):
        opts, args = self.parser.parse_args(args)
        self.set_opts(opts)
        return(opts, args)
