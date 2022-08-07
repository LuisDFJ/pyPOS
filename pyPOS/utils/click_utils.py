import click
from flask.cli import with_appcontext
from pyPOS.utils.products import get_categories

class ClickFlagRequired( click.Option ):
    def __init__( self, *args, **kwargs ):
        self.flag_required = kwargs.pop( 'flag_required', False )
        super( ClickFlagRequired, self ).__init__( *args, **kwargs )
    def handle_parse_result(self, ctx, opts, args):
        prompt = False
        for flag in self.flag_required:
            if opts.get( flag, False ): prompt = True; break
        if not prompt: self.prompt=None
        return super().handle_parse_result(ctx, opts, args)

class ClickProductChoice( click.Option ):
    def __init__( self, *args, **kwargs ):
        super( ClickProductChoice, self ).__init__( *args, **kwargs )
    @with_appcontext
    def handle_parse_result(self, ctx, opts, args):
        self.type = click.Choice( get_categories() )
        return super().handle_parse_result(ctx, opts, args)

class ClickProductContext( click.Option ):
    def __init__( self, *args, **kwargs ):
        self.get_product = kwargs.pop( 'get_product_callback', lambda id: None )
        super( ClickProductContext, self ).__init__( *args, **kwargs )
    @with_appcontext
    def handle_parse_result(self, ctx, opts, args):
        self.default = self.get_product( ctx.params[ 'id' ] )[ self.name ]
        return super().handle_parse_result(ctx, opts, args)

class ClickProductChoiceContext( click.Option ):
    def __init__( self, *args, **kwargs ):
        self.get_product = kwargs.pop( 'get_product_callback', lambda id: None )
        super( ClickProductChoiceContext, self ).__init__( *args, **kwargs )
    @with_appcontext
    def handle_parse_result(self, ctx, opts, args):
        self.type = click.Choice( get_categories() )
        self.default = self.get_product( ctx.params[ 'id' ] )[ self.name ]
        return super().handle_parse_result(ctx, opts, args)
