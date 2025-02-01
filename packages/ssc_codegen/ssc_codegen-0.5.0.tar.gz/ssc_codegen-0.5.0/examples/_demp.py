"""example usage API interface"""
if __name__ == '__main__':
    from ssc_codegen.ast_builder import build_ast_module
    from ssc_codegen.converters.dart_universal_html import converter
    ast = build_ast_module(
        'schemas/booksToScrape.py',
        # set true, if target language required hover top on class/function docstring
        # (dart, js, go...)
        docstring_class_top=True
    )
    code = converter.convert_program(ast)
    print("\n".join(code))
