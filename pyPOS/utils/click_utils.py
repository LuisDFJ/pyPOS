import click

class ClickFlagRequired( click.Option ):
    def __init__( self, *args, **kwargs ):
        self.flag_required = kwargs.pop( 'flag_required', False )
        super( ClickFlagRequired, self ).__init__( *args, **kwargs )
    def handle_parse_result(self, ctx, opts, args):
        if not opts.get( self.flag_required, False ): self.prompt=None
        return super().handle_parse_result(ctx, opts, args)
