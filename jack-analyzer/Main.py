import os

from parser import CompilationEngine, JackTokenizer


def write_flat_tokens(tokenizer, output_file):
    with open(output_file, "w") as out:
        out.write("<tokens>\n")

        while tokenizer.has_more():
            tokenizer.advance()
            tag = tokenizer.token_type()
            value = tokenizer.current_token

            if tag == "stringConstant":
                value = value[1:-1]

            value = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            out.write(f"<{tag}> {value} </{tag}>\n")

        out.write("</tokens>\n")


def main():
    for filename in os.listdir("."):
        if filename.endswith(".jack") and os.path.isfile(filename):
            tokenizer_for_tokens = JackTokenizer(filename)
            token_xml_name = filename.replace(".jack", "T.xml")
            write_flat_tokens(tokenizer_for_tokens, token_xml_name)

            tokenizer_for_parser = JackTokenizer(filename)
            parsed_xml_name = filename.replace(".jack", ".xml")
            engine = CompilationEngine(tokenizer_for_parser, parsed_xml_name)
            engine.compile_class()

            print(f"Created both {token_xml_name} and {parsed_xml_name}")


if __name__ == "__main__":
    main()
