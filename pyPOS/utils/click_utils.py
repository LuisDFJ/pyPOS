import click
from flask.cli import with_appcontext

class ClickFlagRequired( click.Option ):
    def __init__( self, *args, **kwargs ):
        self.flag_required = kwargs.pop( 'flag_required', False )
        super( ClickFlagRequired, self ).__init__( *args, **kwargs )
    def handle_parse_result(self, ctx, opts, args):
        if not opts.get( self.flag_required, False ): self.prompt=None
        return super().handle_parse_result(ctx, opts, args)

class ClickProductContext( click.Option ):
    def __init__( self, *args, **kwargs ):
        self.get_product = kwargs.pop( 'get_product_callback', lambda id: None )
        super( ClickProductContext, self ).__init__( *args, **kwargs )
    @with_appcontext
    def handle_parse_result(self, ctx, opts, args):
        self.default = self.get_product( ctx.params[ 'id' ] )[ self.name ]
        return super().handle_parse_result(ctx, opts, args)
