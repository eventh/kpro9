import org.antlr.runtime.*;

public class Sjark {
	public Sjark() {
	}

	public static void main(String args[]) throws Exception {
		if (args.length == 0) {
			System.out.println("Please input a header file.");
			return;
		}

		ANTLRFileStream input = new ANTLRFileStream(args[0]);
		CLexer lex = new CLexer(input);
       	CommonTokenStream tokens = new CommonTokenStream(lex);
        CParser parser = new CParser(tokens);

		parser.translation_unit();

		System.out.println("Success");
	}

}
