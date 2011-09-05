// $ANTLR 3.4 C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g 2011-09-04 12:07:27

import org.antlr.runtime.*;
import java.util.Stack;
import java.util.List;
import java.util.ArrayList;

@SuppressWarnings({"all", "warnings", "unchecked"})
public class CLexer extends Lexer {
    public static final int EOF=-1;
    public static final int T__23=23;
    public static final int T__24=24;
    public static final int T__25=25;
    public static final int T__26=26;
    public static final int T__27=27;
    public static final int T__28=28;
    public static final int T__29=29;
    public static final int T__30=30;
    public static final int T__31=31;
    public static final int T__32=32;
    public static final int T__33=33;
    public static final int T__34=34;
    public static final int T__35=35;
    public static final int T__36=36;
    public static final int T__37=37;
    public static final int T__38=38;
    public static final int T__39=39;
    public static final int T__40=40;
    public static final int T__41=41;
    public static final int T__42=42;
    public static final int T__43=43;
    public static final int T__44=44;
    public static final int T__45=45;
    public static final int T__46=46;
    public static final int T__47=47;
    public static final int T__48=48;
    public static final int T__49=49;
    public static final int T__50=50;
    public static final int T__51=51;
    public static final int T__52=52;
    public static final int T__53=53;
    public static final int T__54=54;
    public static final int T__55=55;
    public static final int T__56=56;
    public static final int T__57=57;
    public static final int T__58=58;
    public static final int T__59=59;
    public static final int T__60=60;
    public static final int T__61=61;
    public static final int T__62=62;
    public static final int T__63=63;
    public static final int T__64=64;
    public static final int T__65=65;
    public static final int T__66=66;
    public static final int T__67=67;
    public static final int T__68=68;
    public static final int T__69=69;
    public static final int T__70=70;
    public static final int T__71=71;
    public static final int T__72=72;
    public static final int T__73=73;
    public static final int T__74=74;
    public static final int T__75=75;
    public static final int T__76=76;
    public static final int T__77=77;
    public static final int T__78=78;
    public static final int T__79=79;
    public static final int T__80=80;
    public static final int T__81=81;
    public static final int T__82=82;
    public static final int T__83=83;
    public static final int T__84=84;
    public static final int T__85=85;
    public static final int T__86=86;
    public static final int T__87=87;
    public static final int T__88=88;
    public static final int T__89=89;
    public static final int T__90=90;
    public static final int T__91=91;
    public static final int T__92=92;
    public static final int T__93=93;
    public static final int T__94=94;
    public static final int T__95=95;
    public static final int T__96=96;
    public static final int T__97=97;
    public static final int T__98=98;
    public static final int T__99=99;
    public static final int T__100=100;
    public static final int CHARACTER_LITERAL=4;
    public static final int COMMENT=5;
    public static final int DECIMAL_LITERAL=6;
    public static final int EscapeSequence=7;
    public static final int Exponent=8;
    public static final int FLOATING_POINT_LITERAL=9;
    public static final int FloatTypeSuffix=10;
    public static final int HEX_LITERAL=11;
    public static final int HexDigit=12;
    public static final int IDENTIFIER=13;
    public static final int IntegerTypeSuffix=14;
    public static final int LETTER=15;
    public static final int LINE_COMMAND=16;
    public static final int LINE_COMMENT=17;
    public static final int OCTAL_LITERAL=18;
    public static final int OctalEscape=19;
    public static final int STRING_LITERAL=20;
    public static final int UnicodeEscape=21;
    public static final int WS=22;

    // delegates
    // delegators
    public Lexer[] getDelegates() {
        return new Lexer[] {};
    }

    public CLexer() {} 
    public CLexer(CharStream input) {
        this(input, new RecognizerSharedState());
    }
    public CLexer(CharStream input, RecognizerSharedState state) {
        super(input,state);
    }
    public String getGrammarFileName() { return "C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g"; }

    // $ANTLR start "T__23"
    public final void mT__23() throws RecognitionException {
        try {
            int _type = T__23;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:2:7: ( '!' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:2:9: '!'
            {
            match('!'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__23"

    // $ANTLR start "T__24"
    public final void mT__24() throws RecognitionException {
        try {
            int _type = T__24;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:3:7: ( '!=' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:3:9: '!='
            {
            match("!="); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__24"

    // $ANTLR start "T__25"
    public final void mT__25() throws RecognitionException {
        try {
            int _type = T__25;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:4:7: ( '%' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:4:9: '%'
            {
            match('%'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__25"

    // $ANTLR start "T__26"
    public final void mT__26() throws RecognitionException {
        try {
            int _type = T__26;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:5:7: ( '%=' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:5:9: '%='
            {
            match("%="); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__26"

    // $ANTLR start "T__27"
    public final void mT__27() throws RecognitionException {
        try {
            int _type = T__27;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:6:7: ( '&&' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:6:9: '&&'
            {
            match("&&"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__27"

    // $ANTLR start "T__28"
    public final void mT__28() throws RecognitionException {
        try {
            int _type = T__28;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:7:7: ( '&' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:7:9: '&'
            {
            match('&'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__28"

    // $ANTLR start "T__29"
    public final void mT__29() throws RecognitionException {
        try {
            int _type = T__29;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:8:7: ( '&=' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:8:9: '&='
            {
            match("&="); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__29"

    // $ANTLR start "T__30"
    public final void mT__30() throws RecognitionException {
        try {
            int _type = T__30;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:9:7: ( '(' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:9:9: '('
            {
            match('('); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__30"

    // $ANTLR start "T__31"
    public final void mT__31() throws RecognitionException {
        try {
            int _type = T__31;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:10:7: ( ')' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:10:9: ')'
            {
            match(')'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__31"

    // $ANTLR start "T__32"
    public final void mT__32() throws RecognitionException {
        try {
            int _type = T__32;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:11:7: ( '*' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:11:9: '*'
            {
            match('*'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__32"

    // $ANTLR start "T__33"
    public final void mT__33() throws RecognitionException {
        try {
            int _type = T__33;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:12:7: ( '*=' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:12:9: '*='
            {
            match("*="); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__33"

    // $ANTLR start "T__34"
    public final void mT__34() throws RecognitionException {
        try {
            int _type = T__34;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:13:7: ( '+' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:13:9: '+'
            {
            match('+'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__34"

    // $ANTLR start "T__35"
    public final void mT__35() throws RecognitionException {
        try {
            int _type = T__35;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:14:7: ( '++' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:14:9: '++'
            {
            match("++"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__35"

    // $ANTLR start "T__36"
    public final void mT__36() throws RecognitionException {
        try {
            int _type = T__36;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:15:7: ( '+=' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:15:9: '+='
            {
            match("+="); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__36"

    // $ANTLR start "T__37"
    public final void mT__37() throws RecognitionException {
        try {
            int _type = T__37;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:16:7: ( ',' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:16:9: ','
            {
            match(','); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__37"

    // $ANTLR start "T__38"
    public final void mT__38() throws RecognitionException {
        try {
            int _type = T__38;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:17:7: ( '-' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:17:9: '-'
            {
            match('-'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__38"

    // $ANTLR start "T__39"
    public final void mT__39() throws RecognitionException {
        try {
            int _type = T__39;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:18:7: ( '--' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:18:9: '--'
            {
            match("--"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__39"

    // $ANTLR start "T__40"
    public final void mT__40() throws RecognitionException {
        try {
            int _type = T__40;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:19:7: ( '-=' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:19:9: '-='
            {
            match("-="); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__40"

    // $ANTLR start "T__41"
    public final void mT__41() throws RecognitionException {
        try {
            int _type = T__41;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:20:7: ( '->' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:20:9: '->'
            {
            match("->"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__41"

    // $ANTLR start "T__42"
    public final void mT__42() throws RecognitionException {
        try {
            int _type = T__42;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:21:7: ( '.' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:21:9: '.'
            {
            match('.'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__42"

    // $ANTLR start "T__43"
    public final void mT__43() throws RecognitionException {
        try {
            int _type = T__43;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:22:7: ( '...' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:22:9: '...'
            {
            match("..."); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__43"

    // $ANTLR start "T__44"
    public final void mT__44() throws RecognitionException {
        try {
            int _type = T__44;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:23:7: ( '/' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:23:9: '/'
            {
            match('/'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__44"

    // $ANTLR start "T__45"
    public final void mT__45() throws RecognitionException {
        try {
            int _type = T__45;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:24:7: ( '/=' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:24:9: '/='
            {
            match("/="); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__45"

    // $ANTLR start "T__46"
    public final void mT__46() throws RecognitionException {
        try {
            int _type = T__46;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:25:7: ( ':' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:25:9: ':'
            {
            match(':'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__46"

    // $ANTLR start "T__47"
    public final void mT__47() throws RecognitionException {
        try {
            int _type = T__47;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:26:7: ( ';' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:26:9: ';'
            {
            match(';'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__47"

    // $ANTLR start "T__48"
    public final void mT__48() throws RecognitionException {
        try {
            int _type = T__48;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:27:7: ( '<' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:27:9: '<'
            {
            match('<'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__48"

    // $ANTLR start "T__49"
    public final void mT__49() throws RecognitionException {
        try {
            int _type = T__49;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:28:7: ( '<<' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:28:9: '<<'
            {
            match("<<"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__49"

    // $ANTLR start "T__50"
    public final void mT__50() throws RecognitionException {
        try {
            int _type = T__50;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:29:7: ( '<<=' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:29:9: '<<='
            {
            match("<<="); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__50"

    // $ANTLR start "T__51"
    public final void mT__51() throws RecognitionException {
        try {
            int _type = T__51;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:30:7: ( '<=' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:30:9: '<='
            {
            match("<="); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__51"

    // $ANTLR start "T__52"
    public final void mT__52() throws RecognitionException {
        try {
            int _type = T__52;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:31:7: ( '=' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:31:9: '='
            {
            match('='); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__52"

    // $ANTLR start "T__53"
    public final void mT__53() throws RecognitionException {
        try {
            int _type = T__53;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:32:7: ( '==' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:32:9: '=='
            {
            match("=="); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__53"

    // $ANTLR start "T__54"
    public final void mT__54() throws RecognitionException {
        try {
            int _type = T__54;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:33:7: ( '>' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:33:9: '>'
            {
            match('>'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__54"

    // $ANTLR start "T__55"
    public final void mT__55() throws RecognitionException {
        try {
            int _type = T__55;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:34:7: ( '>=' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:34:9: '>='
            {
            match(">="); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__55"

    // $ANTLR start "T__56"
    public final void mT__56() throws RecognitionException {
        try {
            int _type = T__56;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:35:7: ( '>>' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:35:9: '>>'
            {
            match(">>"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__56"

    // $ANTLR start "T__57"
    public final void mT__57() throws RecognitionException {
        try {
            int _type = T__57;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:36:7: ( '>>=' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:36:9: '>>='
            {
            match(">>="); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__57"

    // $ANTLR start "T__58"
    public final void mT__58() throws RecognitionException {
        try {
            int _type = T__58;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:37:7: ( '?' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:37:9: '?'
            {
            match('?'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__58"

    // $ANTLR start "T__59"
    public final void mT__59() throws RecognitionException {
        try {
            int _type = T__59;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:38:7: ( '[' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:38:9: '['
            {
            match('['); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__59"

    // $ANTLR start "T__60"
    public final void mT__60() throws RecognitionException {
        try {
            int _type = T__60;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:39:7: ( ']' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:39:9: ']'
            {
            match(']'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__60"

    // $ANTLR start "T__61"
    public final void mT__61() throws RecognitionException {
        try {
            int _type = T__61;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:40:7: ( '^' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:40:9: '^'
            {
            match('^'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__61"

    // $ANTLR start "T__62"
    public final void mT__62() throws RecognitionException {
        try {
            int _type = T__62;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:41:7: ( '^=' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:41:9: '^='
            {
            match("^="); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__62"

    // $ANTLR start "T__63"
    public final void mT__63() throws RecognitionException {
        try {
            int _type = T__63;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:42:7: ( 'auto' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:42:9: 'auto'
            {
            match("auto"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__63"

    // $ANTLR start "T__64"
    public final void mT__64() throws RecognitionException {
        try {
            int _type = T__64;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:43:7: ( 'break' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:43:9: 'break'
            {
            match("break"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__64"

    // $ANTLR start "T__65"
    public final void mT__65() throws RecognitionException {
        try {
            int _type = T__65;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:44:7: ( 'case' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:44:9: 'case'
            {
            match("case"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__65"

    // $ANTLR start "T__66"
    public final void mT__66() throws RecognitionException {
        try {
            int _type = T__66;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:45:7: ( 'char' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:45:9: 'char'
            {
            match("char"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__66"

    // $ANTLR start "T__67"
    public final void mT__67() throws RecognitionException {
        try {
            int _type = T__67;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:46:7: ( 'const' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:46:9: 'const'
            {
            match("const"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__67"

    // $ANTLR start "T__68"
    public final void mT__68() throws RecognitionException {
        try {
            int _type = T__68;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:47:7: ( 'continue' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:47:9: 'continue'
            {
            match("continue"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__68"

    // $ANTLR start "T__69"
    public final void mT__69() throws RecognitionException {
        try {
            int _type = T__69;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:48:7: ( 'default' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:48:9: 'default'
            {
            match("default"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__69"

    // $ANTLR start "T__70"
    public final void mT__70() throws RecognitionException {
        try {
            int _type = T__70;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:49:7: ( 'do' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:49:9: 'do'
            {
            match("do"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__70"

    // $ANTLR start "T__71"
    public final void mT__71() throws RecognitionException {
        try {
            int _type = T__71;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:50:7: ( 'double' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:50:9: 'double'
            {
            match("double"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__71"

    // $ANTLR start "T__72"
    public final void mT__72() throws RecognitionException {
        try {
            int _type = T__72;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:51:7: ( 'else' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:51:9: 'else'
            {
            match("else"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__72"

    // $ANTLR start "T__73"
    public final void mT__73() throws RecognitionException {
        try {
            int _type = T__73;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:52:7: ( 'enum' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:52:9: 'enum'
            {
            match("enum"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__73"

    // $ANTLR start "T__74"
    public final void mT__74() throws RecognitionException {
        try {
            int _type = T__74;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:53:7: ( 'extern' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:53:9: 'extern'
            {
            match("extern"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__74"

    // $ANTLR start "T__75"
    public final void mT__75() throws RecognitionException {
        try {
            int _type = T__75;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:54:7: ( 'float' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:54:9: 'float'
            {
            match("float"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__75"

    // $ANTLR start "T__76"
    public final void mT__76() throws RecognitionException {
        try {
            int _type = T__76;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:55:7: ( 'for' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:55:9: 'for'
            {
            match("for"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__76"

    // $ANTLR start "T__77"
    public final void mT__77() throws RecognitionException {
        try {
            int _type = T__77;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:56:7: ( 'goto' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:56:9: 'goto'
            {
            match("goto"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__77"

    // $ANTLR start "T__78"
    public final void mT__78() throws RecognitionException {
        try {
            int _type = T__78;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:57:7: ( 'if' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:57:9: 'if'
            {
            match("if"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__78"

    // $ANTLR start "T__79"
    public final void mT__79() throws RecognitionException {
        try {
            int _type = T__79;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:58:7: ( 'int' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:58:9: 'int'
            {
            match("int"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__79"

    // $ANTLR start "T__80"
    public final void mT__80() throws RecognitionException {
        try {
            int _type = T__80;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:59:7: ( 'long' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:59:9: 'long'
            {
            match("long"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__80"

    // $ANTLR start "T__81"
    public final void mT__81() throws RecognitionException {
        try {
            int _type = T__81;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:60:7: ( 'register' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:60:9: 'register'
            {
            match("register"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__81"

    // $ANTLR start "T__82"
    public final void mT__82() throws RecognitionException {
        try {
            int _type = T__82;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:61:7: ( 'return' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:61:9: 'return'
            {
            match("return"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__82"

    // $ANTLR start "T__83"
    public final void mT__83() throws RecognitionException {
        try {
            int _type = T__83;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:62:7: ( 'short' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:62:9: 'short'
            {
            match("short"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__83"

    // $ANTLR start "T__84"
    public final void mT__84() throws RecognitionException {
        try {
            int _type = T__84;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:63:7: ( 'signed' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:63:9: 'signed'
            {
            match("signed"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__84"

    // $ANTLR start "T__85"
    public final void mT__85() throws RecognitionException {
        try {
            int _type = T__85;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:64:7: ( 'sizeof' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:64:9: 'sizeof'
            {
            match("sizeof"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__85"

    // $ANTLR start "T__86"
    public final void mT__86() throws RecognitionException {
        try {
            int _type = T__86;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:65:7: ( 'static' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:65:9: 'static'
            {
            match("static"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__86"

    // $ANTLR start "T__87"
    public final void mT__87() throws RecognitionException {
        try {
            int _type = T__87;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:66:7: ( 'struct' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:66:9: 'struct'
            {
            match("struct"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__87"

    // $ANTLR start "T__88"
    public final void mT__88() throws RecognitionException {
        try {
            int _type = T__88;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:67:7: ( 'switch' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:67:9: 'switch'
            {
            match("switch"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__88"

    // $ANTLR start "T__89"
    public final void mT__89() throws RecognitionException {
        try {
            int _type = T__89;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:68:7: ( 'typedef' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:68:9: 'typedef'
            {
            match("typedef"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__89"

    // $ANTLR start "T__90"
    public final void mT__90() throws RecognitionException {
        try {
            int _type = T__90;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:69:7: ( 'union' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:69:9: 'union'
            {
            match("union"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__90"

    // $ANTLR start "T__91"
    public final void mT__91() throws RecognitionException {
        try {
            int _type = T__91;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:70:7: ( 'unsigned' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:70:9: 'unsigned'
            {
            match("unsigned"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__91"

    // $ANTLR start "T__92"
    public final void mT__92() throws RecognitionException {
        try {
            int _type = T__92;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:71:7: ( 'void' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:71:9: 'void'
            {
            match("void"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__92"

    // $ANTLR start "T__93"
    public final void mT__93() throws RecognitionException {
        try {
            int _type = T__93;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:72:7: ( 'volatile' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:72:9: 'volatile'
            {
            match("volatile"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__93"

    // $ANTLR start "T__94"
    public final void mT__94() throws RecognitionException {
        try {
            int _type = T__94;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:73:7: ( 'while' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:73:9: 'while'
            {
            match("while"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__94"

    // $ANTLR start "T__95"
    public final void mT__95() throws RecognitionException {
        try {
            int _type = T__95;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:74:7: ( '{' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:74:9: '{'
            {
            match('{'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__95"

    // $ANTLR start "T__96"
    public final void mT__96() throws RecognitionException {
        try {
            int _type = T__96;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:75:7: ( '|' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:75:9: '|'
            {
            match('|'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__96"

    // $ANTLR start "T__97"
    public final void mT__97() throws RecognitionException {
        try {
            int _type = T__97;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:76:7: ( '|=' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:76:9: '|='
            {
            match("|="); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__97"

    // $ANTLR start "T__98"
    public final void mT__98() throws RecognitionException {
        try {
            int _type = T__98;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:77:7: ( '||' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:77:9: '||'
            {
            match("||"); 



            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__98"

    // $ANTLR start "T__99"
    public final void mT__99() throws RecognitionException {
        try {
            int _type = T__99;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:78:7: ( '}' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:78:9: '}'
            {
            match('}'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__99"

    // $ANTLR start "T__100"
    public final void mT__100() throws RecognitionException {
        try {
            int _type = T__100;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:79:8: ( '~' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:79:10: '~'
            {
            match('~'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "T__100"

    // $ANTLR start "IDENTIFIER"
    public final void mIDENTIFIER() throws RecognitionException {
        try {
            int _type = IDENTIFIER;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:473:2: ( LETTER ( LETTER | '0' .. '9' )* )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:473:4: LETTER ( LETTER | '0' .. '9' )*
            {
            mLETTER(); 


            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:473:11: ( LETTER | '0' .. '9' )*
            loop1:
            do {
                int alt1=2;
                int LA1_0 = input.LA(1);

                if ( (LA1_0=='$'||(LA1_0 >= '0' && LA1_0 <= '9')||(LA1_0 >= 'A' && LA1_0 <= 'Z')||LA1_0=='_'||(LA1_0 >= 'a' && LA1_0 <= 'z')) ) {
                    alt1=1;
                }


                switch (alt1) {
            	case 1 :
            	    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:
            	    {
            	    if ( input.LA(1)=='$'||(input.LA(1) >= '0' && input.LA(1) <= '9')||(input.LA(1) >= 'A' && input.LA(1) <= 'Z')||input.LA(1)=='_'||(input.LA(1) >= 'a' && input.LA(1) <= 'z') ) {
            	        input.consume();
            	    }
            	    else {
            	        MismatchedSetException mse = new MismatchedSetException(null,input);
            	        recover(mse);
            	        throw mse;
            	    }


            	    }
            	    break;

            	default :
            	    break loop1;
                }
            } while (true);


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "IDENTIFIER"

    // $ANTLR start "LETTER"
    public final void mLETTER() throws RecognitionException {
        try {
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:479:2: ( '$' | 'A' .. 'Z' | 'a' .. 'z' | '_' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:
            {
            if ( input.LA(1)=='$'||(input.LA(1) >= 'A' && input.LA(1) <= 'Z')||input.LA(1)=='_'||(input.LA(1) >= 'a' && input.LA(1) <= 'z') ) {
                input.consume();
            }
            else {
                MismatchedSetException mse = new MismatchedSetException(null,input);
                recover(mse);
                throw mse;
            }


            }


        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "LETTER"

    // $ANTLR start "CHARACTER_LITERAL"
    public final void mCHARACTER_LITERAL() throws RecognitionException {
        try {
            int _type = CHARACTER_LITERAL;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:485:5: ( '\\'' ( EscapeSequence |~ ( '\\'' | '\\\\' ) ) '\\'' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:485:9: '\\'' ( EscapeSequence |~ ( '\\'' | '\\\\' ) ) '\\''
            {
            match('\''); 

            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:485:14: ( EscapeSequence |~ ( '\\'' | '\\\\' ) )
            int alt2=2;
            int LA2_0 = input.LA(1);

            if ( (LA2_0=='\\') ) {
                alt2=1;
            }
            else if ( ((LA2_0 >= '\u0000' && LA2_0 <= '&')||(LA2_0 >= '(' && LA2_0 <= '[')||(LA2_0 >= ']' && LA2_0 <= '\uFFFF')) ) {
                alt2=2;
            }
            else {
                NoViableAltException nvae =
                    new NoViableAltException("", 2, 0, input);

                throw nvae;

            }
            switch (alt2) {
                case 1 :
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:485:16: EscapeSequence
                    {
                    mEscapeSequence(); 


                    }
                    break;
                case 2 :
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:485:33: ~ ( '\\'' | '\\\\' )
                    {
                    if ( (input.LA(1) >= '\u0000' && input.LA(1) <= '&')||(input.LA(1) >= '(' && input.LA(1) <= '[')||(input.LA(1) >= ']' && input.LA(1) <= '\uFFFF') ) {
                        input.consume();
                    }
                    else {
                        MismatchedSetException mse = new MismatchedSetException(null,input);
                        recover(mse);
                        throw mse;
                    }


                    }
                    break;

            }


            match('\''); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "CHARACTER_LITERAL"

    // $ANTLR start "STRING_LITERAL"
    public final void mSTRING_LITERAL() throws RecognitionException {
        try {
            int _type = STRING_LITERAL;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:489:5: ( '\"' ( EscapeSequence |~ ( '\\\\' | '\"' ) )* '\"' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:489:8: '\"' ( EscapeSequence |~ ( '\\\\' | '\"' ) )* '\"'
            {
            match('\"'); 

            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:489:12: ( EscapeSequence |~ ( '\\\\' | '\"' ) )*
            loop3:
            do {
                int alt3=3;
                int LA3_0 = input.LA(1);

                if ( (LA3_0=='\\') ) {
                    alt3=1;
                }
                else if ( ((LA3_0 >= '\u0000' && LA3_0 <= '!')||(LA3_0 >= '#' && LA3_0 <= '[')||(LA3_0 >= ']' && LA3_0 <= '\uFFFF')) ) {
                    alt3=2;
                }


                switch (alt3) {
            	case 1 :
            	    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:489:14: EscapeSequence
            	    {
            	    mEscapeSequence(); 


            	    }
            	    break;
            	case 2 :
            	    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:489:31: ~ ( '\\\\' | '\"' )
            	    {
            	    if ( (input.LA(1) >= '\u0000' && input.LA(1) <= '!')||(input.LA(1) >= '#' && input.LA(1) <= '[')||(input.LA(1) >= ']' && input.LA(1) <= '\uFFFF') ) {
            	        input.consume();
            	    }
            	    else {
            	        MismatchedSetException mse = new MismatchedSetException(null,input);
            	        recover(mse);
            	        throw mse;
            	    }


            	    }
            	    break;

            	default :
            	    break loop3;
                }
            } while (true);


            match('\"'); 

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "STRING_LITERAL"

    // $ANTLR start "HEX_LITERAL"
    public final void mHEX_LITERAL() throws RecognitionException {
        try {
            int _type = HEX_LITERAL;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:492:13: ( '0' ( 'x' | 'X' ) ( HexDigit )+ ( IntegerTypeSuffix )? )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:492:15: '0' ( 'x' | 'X' ) ( HexDigit )+ ( IntegerTypeSuffix )?
            {
            match('0'); 

            if ( input.LA(1)=='X'||input.LA(1)=='x' ) {
                input.consume();
            }
            else {
                MismatchedSetException mse = new MismatchedSetException(null,input);
                recover(mse);
                throw mse;
            }


            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:492:29: ( HexDigit )+
            int cnt4=0;
            loop4:
            do {
                int alt4=2;
                int LA4_0 = input.LA(1);

                if ( ((LA4_0 >= '0' && LA4_0 <= '9')||(LA4_0 >= 'A' && LA4_0 <= 'F')||(LA4_0 >= 'a' && LA4_0 <= 'f')) ) {
                    alt4=1;
                }


                switch (alt4) {
            	case 1 :
            	    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:
            	    {
            	    if ( (input.LA(1) >= '0' && input.LA(1) <= '9')||(input.LA(1) >= 'A' && input.LA(1) <= 'F')||(input.LA(1) >= 'a' && input.LA(1) <= 'f') ) {
            	        input.consume();
            	    }
            	    else {
            	        MismatchedSetException mse = new MismatchedSetException(null,input);
            	        recover(mse);
            	        throw mse;
            	    }


            	    }
            	    break;

            	default :
            	    if ( cnt4 >= 1 ) break loop4;
                        EarlyExitException eee =
                            new EarlyExitException(4, input);
                        throw eee;
                }
                cnt4++;
            } while (true);


            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:492:39: ( IntegerTypeSuffix )?
            int alt5=2;
            int LA5_0 = input.LA(1);

            if ( (LA5_0=='L'||LA5_0=='U'||LA5_0=='l'||LA5_0=='u') ) {
                alt5=1;
            }
            switch (alt5) {
                case 1 :
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:492:39: IntegerTypeSuffix
                    {
                    mIntegerTypeSuffix(); 


                    }
                    break;

            }


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "HEX_LITERAL"

    // $ANTLR start "DECIMAL_LITERAL"
    public final void mDECIMAL_LITERAL() throws RecognitionException {
        try {
            int _type = DECIMAL_LITERAL;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:494:17: ( ( '0' | '1' .. '9' ( '0' .. '9' )* ) ( IntegerTypeSuffix )? )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:494:19: ( '0' | '1' .. '9' ( '0' .. '9' )* ) ( IntegerTypeSuffix )?
            {
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:494:19: ( '0' | '1' .. '9' ( '0' .. '9' )* )
            int alt7=2;
            int LA7_0 = input.LA(1);

            if ( (LA7_0=='0') ) {
                alt7=1;
            }
            else if ( ((LA7_0 >= '1' && LA7_0 <= '9')) ) {
                alt7=2;
            }
            else {
                NoViableAltException nvae =
                    new NoViableAltException("", 7, 0, input);

                throw nvae;

            }
            switch (alt7) {
                case 1 :
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:494:20: '0'
                    {
                    match('0'); 

                    }
                    break;
                case 2 :
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:494:26: '1' .. '9' ( '0' .. '9' )*
                    {
                    matchRange('1','9'); 

                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:494:35: ( '0' .. '9' )*
                    loop6:
                    do {
                        int alt6=2;
                        int LA6_0 = input.LA(1);

                        if ( ((LA6_0 >= '0' && LA6_0 <= '9')) ) {
                            alt6=1;
                        }


                        switch (alt6) {
                    	case 1 :
                    	    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:
                    	    {
                    	    if ( (input.LA(1) >= '0' && input.LA(1) <= '9') ) {
                    	        input.consume();
                    	    }
                    	    else {
                    	        MismatchedSetException mse = new MismatchedSetException(null,input);
                    	        recover(mse);
                    	        throw mse;
                    	    }


                    	    }
                    	    break;

                    	default :
                    	    break loop6;
                        }
                    } while (true);


                    }
                    break;

            }


            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:494:46: ( IntegerTypeSuffix )?
            int alt8=2;
            int LA8_0 = input.LA(1);

            if ( (LA8_0=='L'||LA8_0=='U'||LA8_0=='l'||LA8_0=='u') ) {
                alt8=1;
            }
            switch (alt8) {
                case 1 :
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:494:46: IntegerTypeSuffix
                    {
                    mIntegerTypeSuffix(); 


                    }
                    break;

            }


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "DECIMAL_LITERAL"

    // $ANTLR start "OCTAL_LITERAL"
    public final void mOCTAL_LITERAL() throws RecognitionException {
        try {
            int _type = OCTAL_LITERAL;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:496:15: ( '0' ( '0' .. '7' )+ ( IntegerTypeSuffix )? )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:496:17: '0' ( '0' .. '7' )+ ( IntegerTypeSuffix )?
            {
            match('0'); 

            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:496:21: ( '0' .. '7' )+
            int cnt9=0;
            loop9:
            do {
                int alt9=2;
                int LA9_0 = input.LA(1);

                if ( ((LA9_0 >= '0' && LA9_0 <= '7')) ) {
                    alt9=1;
                }


                switch (alt9) {
            	case 1 :
            	    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:
            	    {
            	    if ( (input.LA(1) >= '0' && input.LA(1) <= '7') ) {
            	        input.consume();
            	    }
            	    else {
            	        MismatchedSetException mse = new MismatchedSetException(null,input);
            	        recover(mse);
            	        throw mse;
            	    }


            	    }
            	    break;

            	default :
            	    if ( cnt9 >= 1 ) break loop9;
                        EarlyExitException eee =
                            new EarlyExitException(9, input);
                        throw eee;
                }
                cnt9++;
            } while (true);


            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:496:33: ( IntegerTypeSuffix )?
            int alt10=2;
            int LA10_0 = input.LA(1);

            if ( (LA10_0=='L'||LA10_0=='U'||LA10_0=='l'||LA10_0=='u') ) {
                alt10=1;
            }
            switch (alt10) {
                case 1 :
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:496:33: IntegerTypeSuffix
                    {
                    mIntegerTypeSuffix(); 


                    }
                    break;

            }


            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "OCTAL_LITERAL"

    // $ANTLR start "HexDigit"
    public final void mHexDigit() throws RecognitionException {
        try {
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:500:10: ( ( '0' .. '9' | 'a' .. 'f' | 'A' .. 'F' ) )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:
            {
            if ( (input.LA(1) >= '0' && input.LA(1) <= '9')||(input.LA(1) >= 'A' && input.LA(1) <= 'F')||(input.LA(1) >= 'a' && input.LA(1) <= 'f') ) {
                input.consume();
            }
            else {
                MismatchedSetException mse = new MismatchedSetException(null,input);
                recover(mse);
                throw mse;
            }


            }


        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "HexDigit"

    // $ANTLR start "IntegerTypeSuffix"
    public final void mIntegerTypeSuffix() throws RecognitionException {
        try {
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:504:2: ( ( 'u' | 'U' )? ( 'l' | 'L' ) | ( 'u' | 'U' ) ( 'l' | 'L' )? )
            int alt13=2;
            int LA13_0 = input.LA(1);

            if ( (LA13_0=='U'||LA13_0=='u') ) {
                int LA13_1 = input.LA(2);

                if ( (LA13_1=='L'||LA13_1=='l') ) {
                    alt13=1;
                }
                else {
                    alt13=2;
                }
            }
            else if ( (LA13_0=='L'||LA13_0=='l') ) {
                alt13=1;
            }
            else {
                NoViableAltException nvae =
                    new NoViableAltException("", 13, 0, input);

                throw nvae;

            }
            switch (alt13) {
                case 1 :
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:504:4: ( 'u' | 'U' )? ( 'l' | 'L' )
                    {
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:504:4: ( 'u' | 'U' )?
                    int alt11=2;
                    int LA11_0 = input.LA(1);

                    if ( (LA11_0=='U'||LA11_0=='u') ) {
                        alt11=1;
                    }
                    switch (alt11) {
                        case 1 :
                            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:
                            {
                            if ( input.LA(1)=='U'||input.LA(1)=='u' ) {
                                input.consume();
                            }
                            else {
                                MismatchedSetException mse = new MismatchedSetException(null,input);
                                recover(mse);
                                throw mse;
                            }


                            }
                            break;

                    }


                    if ( input.LA(1)=='L'||input.LA(1)=='l' ) {
                        input.consume();
                    }
                    else {
                        MismatchedSetException mse = new MismatchedSetException(null,input);
                        recover(mse);
                        throw mse;
                    }


                    }
                    break;
                case 2 :
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:505:4: ( 'u' | 'U' ) ( 'l' | 'L' )?
                    {
                    if ( input.LA(1)=='U'||input.LA(1)=='u' ) {
                        input.consume();
                    }
                    else {
                        MismatchedSetException mse = new MismatchedSetException(null,input);
                        recover(mse);
                        throw mse;
                    }


                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:505:15: ( 'l' | 'L' )?
                    int alt12=2;
                    int LA12_0 = input.LA(1);

                    if ( (LA12_0=='L'||LA12_0=='l') ) {
                        alt12=1;
                    }
                    switch (alt12) {
                        case 1 :
                            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:
                            {
                            if ( input.LA(1)=='L'||input.LA(1)=='l' ) {
                                input.consume();
                            }
                            else {
                                MismatchedSetException mse = new MismatchedSetException(null,input);
                                recover(mse);
                                throw mse;
                            }


                            }
                            break;

                    }


                    }
                    break;

            }

        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "IntegerTypeSuffix"

    // $ANTLR start "FLOATING_POINT_LITERAL"
    public final void mFLOATING_POINT_LITERAL() throws RecognitionException {
        try {
            int _type = FLOATING_POINT_LITERAL;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:508:5: ( ( '0' .. '9' )+ '.' ( '0' .. '9' )* ( Exponent )? ( FloatTypeSuffix )? | '.' ( '0' .. '9' )+ ( Exponent )? ( FloatTypeSuffix )? | ( '0' .. '9' )+ Exponent ( FloatTypeSuffix )? | ( '0' .. '9' )+ ( Exponent )? FloatTypeSuffix )
            int alt25=4;
            alt25 = dfa25.predict(input);
            switch (alt25) {
                case 1 :
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:508:9: ( '0' .. '9' )+ '.' ( '0' .. '9' )* ( Exponent )? ( FloatTypeSuffix )?
                    {
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:508:9: ( '0' .. '9' )+
                    int cnt14=0;
                    loop14:
                    do {
                        int alt14=2;
                        int LA14_0 = input.LA(1);

                        if ( ((LA14_0 >= '0' && LA14_0 <= '9')) ) {
                            alt14=1;
                        }


                        switch (alt14) {
                    	case 1 :
                    	    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:
                    	    {
                    	    if ( (input.LA(1) >= '0' && input.LA(1) <= '9') ) {
                    	        input.consume();
                    	    }
                    	    else {
                    	        MismatchedSetException mse = new MismatchedSetException(null,input);
                    	        recover(mse);
                    	        throw mse;
                    	    }


                    	    }
                    	    break;

                    	default :
                    	    if ( cnt14 >= 1 ) break loop14;
                                EarlyExitException eee =
                                    new EarlyExitException(14, input);
                                throw eee;
                        }
                        cnt14++;
                    } while (true);


                    match('.'); 

                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:508:25: ( '0' .. '9' )*
                    loop15:
                    do {
                        int alt15=2;
                        int LA15_0 = input.LA(1);

                        if ( ((LA15_0 >= '0' && LA15_0 <= '9')) ) {
                            alt15=1;
                        }


                        switch (alt15) {
                    	case 1 :
                    	    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:
                    	    {
                    	    if ( (input.LA(1) >= '0' && input.LA(1) <= '9') ) {
                    	        input.consume();
                    	    }
                    	    else {
                    	        MismatchedSetException mse = new MismatchedSetException(null,input);
                    	        recover(mse);
                    	        throw mse;
                    	    }


                    	    }
                    	    break;

                    	default :
                    	    break loop15;
                        }
                    } while (true);


                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:508:37: ( Exponent )?
                    int alt16=2;
                    int LA16_0 = input.LA(1);

                    if ( (LA16_0=='E'||LA16_0=='e') ) {
                        alt16=1;
                    }
                    switch (alt16) {
                        case 1 :
                            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:508:37: Exponent
                            {
                            mExponent(); 


                            }
                            break;

                    }


                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:508:47: ( FloatTypeSuffix )?
                    int alt17=2;
                    int LA17_0 = input.LA(1);

                    if ( (LA17_0=='D'||LA17_0=='F'||LA17_0=='d'||LA17_0=='f') ) {
                        alt17=1;
                    }
                    switch (alt17) {
                        case 1 :
                            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:
                            {
                            if ( input.LA(1)=='D'||input.LA(1)=='F'||input.LA(1)=='d'||input.LA(1)=='f' ) {
                                input.consume();
                            }
                            else {
                                MismatchedSetException mse = new MismatchedSetException(null,input);
                                recover(mse);
                                throw mse;
                            }


                            }
                            break;

                    }


                    }
                    break;
                case 2 :
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:509:9: '.' ( '0' .. '9' )+ ( Exponent )? ( FloatTypeSuffix )?
                    {
                    match('.'); 

                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:509:13: ( '0' .. '9' )+
                    int cnt18=0;
                    loop18:
                    do {
                        int alt18=2;
                        int LA18_0 = input.LA(1);

                        if ( ((LA18_0 >= '0' && LA18_0 <= '9')) ) {
                            alt18=1;
                        }


                        switch (alt18) {
                    	case 1 :
                    	    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:
                    	    {
                    	    if ( (input.LA(1) >= '0' && input.LA(1) <= '9') ) {
                    	        input.consume();
                    	    }
                    	    else {
                    	        MismatchedSetException mse = new MismatchedSetException(null,input);
                    	        recover(mse);
                    	        throw mse;
                    	    }


                    	    }
                    	    break;

                    	default :
                    	    if ( cnt18 >= 1 ) break loop18;
                                EarlyExitException eee =
                                    new EarlyExitException(18, input);
                                throw eee;
                        }
                        cnt18++;
                    } while (true);


                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:509:25: ( Exponent )?
                    int alt19=2;
                    int LA19_0 = input.LA(1);

                    if ( (LA19_0=='E'||LA19_0=='e') ) {
                        alt19=1;
                    }
                    switch (alt19) {
                        case 1 :
                            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:509:25: Exponent
                            {
                            mExponent(); 


                            }
                            break;

                    }


                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:509:35: ( FloatTypeSuffix )?
                    int alt20=2;
                    int LA20_0 = input.LA(1);

                    if ( (LA20_0=='D'||LA20_0=='F'||LA20_0=='d'||LA20_0=='f') ) {
                        alt20=1;
                    }
                    switch (alt20) {
                        case 1 :
                            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:
                            {
                            if ( input.LA(1)=='D'||input.LA(1)=='F'||input.LA(1)=='d'||input.LA(1)=='f' ) {
                                input.consume();
                            }
                            else {
                                MismatchedSetException mse = new MismatchedSetException(null,input);
                                recover(mse);
                                throw mse;
                            }


                            }
                            break;

                    }


                    }
                    break;
                case 3 :
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:510:9: ( '0' .. '9' )+ Exponent ( FloatTypeSuffix )?
                    {
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:510:9: ( '0' .. '9' )+
                    int cnt21=0;
                    loop21:
                    do {
                        int alt21=2;
                        int LA21_0 = input.LA(1);

                        if ( ((LA21_0 >= '0' && LA21_0 <= '9')) ) {
                            alt21=1;
                        }


                        switch (alt21) {
                    	case 1 :
                    	    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:
                    	    {
                    	    if ( (input.LA(1) >= '0' && input.LA(1) <= '9') ) {
                    	        input.consume();
                    	    }
                    	    else {
                    	        MismatchedSetException mse = new MismatchedSetException(null,input);
                    	        recover(mse);
                    	        throw mse;
                    	    }


                    	    }
                    	    break;

                    	default :
                    	    if ( cnt21 >= 1 ) break loop21;
                                EarlyExitException eee =
                                    new EarlyExitException(21, input);
                                throw eee;
                        }
                        cnt21++;
                    } while (true);


                    mExponent(); 


                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:510:30: ( FloatTypeSuffix )?
                    int alt22=2;
                    int LA22_0 = input.LA(1);

                    if ( (LA22_0=='D'||LA22_0=='F'||LA22_0=='d'||LA22_0=='f') ) {
                        alt22=1;
                    }
                    switch (alt22) {
                        case 1 :
                            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:
                            {
                            if ( input.LA(1)=='D'||input.LA(1)=='F'||input.LA(1)=='d'||input.LA(1)=='f' ) {
                                input.consume();
                            }
                            else {
                                MismatchedSetException mse = new MismatchedSetException(null,input);
                                recover(mse);
                                throw mse;
                            }


                            }
                            break;

                    }


                    }
                    break;
                case 4 :
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:511:9: ( '0' .. '9' )+ ( Exponent )? FloatTypeSuffix
                    {
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:511:9: ( '0' .. '9' )+
                    int cnt23=0;
                    loop23:
                    do {
                        int alt23=2;
                        int LA23_0 = input.LA(1);

                        if ( ((LA23_0 >= '0' && LA23_0 <= '9')) ) {
                            alt23=1;
                        }


                        switch (alt23) {
                    	case 1 :
                    	    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:
                    	    {
                    	    if ( (input.LA(1) >= '0' && input.LA(1) <= '9') ) {
                    	        input.consume();
                    	    }
                    	    else {
                    	        MismatchedSetException mse = new MismatchedSetException(null,input);
                    	        recover(mse);
                    	        throw mse;
                    	    }


                    	    }
                    	    break;

                    	default :
                    	    if ( cnt23 >= 1 ) break loop23;
                                EarlyExitException eee =
                                    new EarlyExitException(23, input);
                                throw eee;
                        }
                        cnt23++;
                    } while (true);


                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:511:21: ( Exponent )?
                    int alt24=2;
                    int LA24_0 = input.LA(1);

                    if ( (LA24_0=='E'||LA24_0=='e') ) {
                        alt24=1;
                    }
                    switch (alt24) {
                        case 1 :
                            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:511:21: Exponent
                            {
                            mExponent(); 


                            }
                            break;

                    }


                    mFloatTypeSuffix(); 


                    }
                    break;

            }
            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "FLOATING_POINT_LITERAL"

    // $ANTLR start "Exponent"
    public final void mExponent() throws RecognitionException {
        try {
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:516:10: ( ( 'e' | 'E' ) ( '+' | '-' )? ( '0' .. '9' )+ )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:516:12: ( 'e' | 'E' ) ( '+' | '-' )? ( '0' .. '9' )+
            {
            if ( input.LA(1)=='E'||input.LA(1)=='e' ) {
                input.consume();
            }
            else {
                MismatchedSetException mse = new MismatchedSetException(null,input);
                recover(mse);
                throw mse;
            }


            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:516:22: ( '+' | '-' )?
            int alt26=2;
            int LA26_0 = input.LA(1);

            if ( (LA26_0=='+'||LA26_0=='-') ) {
                alt26=1;
            }
            switch (alt26) {
                case 1 :
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:
                    {
                    if ( input.LA(1)=='+'||input.LA(1)=='-' ) {
                        input.consume();
                    }
                    else {
                        MismatchedSetException mse = new MismatchedSetException(null,input);
                        recover(mse);
                        throw mse;
                    }


                    }
                    break;

            }


            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:516:33: ( '0' .. '9' )+
            int cnt27=0;
            loop27:
            do {
                int alt27=2;
                int LA27_0 = input.LA(1);

                if ( ((LA27_0 >= '0' && LA27_0 <= '9')) ) {
                    alt27=1;
                }


                switch (alt27) {
            	case 1 :
            	    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:
            	    {
            	    if ( (input.LA(1) >= '0' && input.LA(1) <= '9') ) {
            	        input.consume();
            	    }
            	    else {
            	        MismatchedSetException mse = new MismatchedSetException(null,input);
            	        recover(mse);
            	        throw mse;
            	    }


            	    }
            	    break;

            	default :
            	    if ( cnt27 >= 1 ) break loop27;
                        EarlyExitException eee =
                            new EarlyExitException(27, input);
                        throw eee;
                }
                cnt27++;
            } while (true);


            }


        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "Exponent"

    // $ANTLR start "FloatTypeSuffix"
    public final void mFloatTypeSuffix() throws RecognitionException {
        try {
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:519:17: ( ( 'f' | 'F' | 'd' | 'D' ) )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:
            {
            if ( input.LA(1)=='D'||input.LA(1)=='F'||input.LA(1)=='d'||input.LA(1)=='f' ) {
                input.consume();
            }
            else {
                MismatchedSetException mse = new MismatchedSetException(null,input);
                recover(mse);
                throw mse;
            }


            }


        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "FloatTypeSuffix"

    // $ANTLR start "EscapeSequence"
    public final void mEscapeSequence() throws RecognitionException {
        try {
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:523:5: ( '\\\\' ( 'b' | 't' | 'n' | 'f' | 'r' | '\\\"' | '\\'' | '\\\\' ) | OctalEscape )
            int alt28=2;
            int LA28_0 = input.LA(1);

            if ( (LA28_0=='\\') ) {
                int LA28_1 = input.LA(2);

                if ( (LA28_1=='\"'||LA28_1=='\''||LA28_1=='\\'||LA28_1=='b'||LA28_1=='f'||LA28_1=='n'||LA28_1=='r'||LA28_1=='t') ) {
                    alt28=1;
                }
                else if ( ((LA28_1 >= '0' && LA28_1 <= '7')) ) {
                    alt28=2;
                }
                else {
                    NoViableAltException nvae =
                        new NoViableAltException("", 28, 1, input);

                    throw nvae;

                }
            }
            else {
                NoViableAltException nvae =
                    new NoViableAltException("", 28, 0, input);

                throw nvae;

            }
            switch (alt28) {
                case 1 :
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:523:9: '\\\\' ( 'b' | 't' | 'n' | 'f' | 'r' | '\\\"' | '\\'' | '\\\\' )
                    {
                    match('\\'); 

                    if ( input.LA(1)=='\"'||input.LA(1)=='\''||input.LA(1)=='\\'||input.LA(1)=='b'||input.LA(1)=='f'||input.LA(1)=='n'||input.LA(1)=='r'||input.LA(1)=='t' ) {
                        input.consume();
                    }
                    else {
                        MismatchedSetException mse = new MismatchedSetException(null,input);
                        recover(mse);
                        throw mse;
                    }


                    }
                    break;
                case 2 :
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:524:9: OctalEscape
                    {
                    mOctalEscape(); 


                    }
                    break;

            }

        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "EscapeSequence"

    // $ANTLR start "OctalEscape"
    public final void mOctalEscape() throws RecognitionException {
        try {
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:529:5: ( '\\\\' ( '0' .. '3' ) ( '0' .. '7' ) ( '0' .. '7' ) | '\\\\' ( '0' .. '7' ) ( '0' .. '7' ) | '\\\\' ( '0' .. '7' ) )
            int alt29=3;
            int LA29_0 = input.LA(1);

            if ( (LA29_0=='\\') ) {
                int LA29_1 = input.LA(2);

                if ( ((LA29_1 >= '0' && LA29_1 <= '3')) ) {
                    int LA29_2 = input.LA(3);

                    if ( ((LA29_2 >= '0' && LA29_2 <= '7')) ) {
                        int LA29_4 = input.LA(4);

                        if ( ((LA29_4 >= '0' && LA29_4 <= '7')) ) {
                            alt29=1;
                        }
                        else {
                            alt29=2;
                        }
                    }
                    else {
                        alt29=3;
                    }
                }
                else if ( ((LA29_1 >= '4' && LA29_1 <= '7')) ) {
                    int LA29_3 = input.LA(3);

                    if ( ((LA29_3 >= '0' && LA29_3 <= '7')) ) {
                        alt29=2;
                    }
                    else {
                        alt29=3;
                    }
                }
                else {
                    NoViableAltException nvae =
                        new NoViableAltException("", 29, 1, input);

                    throw nvae;

                }
            }
            else {
                NoViableAltException nvae =
                    new NoViableAltException("", 29, 0, input);

                throw nvae;

            }
            switch (alt29) {
                case 1 :
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:529:9: '\\\\' ( '0' .. '3' ) ( '0' .. '7' ) ( '0' .. '7' )
                    {
                    match('\\'); 

                    if ( (input.LA(1) >= '0' && input.LA(1) <= '3') ) {
                        input.consume();
                    }
                    else {
                        MismatchedSetException mse = new MismatchedSetException(null,input);
                        recover(mse);
                        throw mse;
                    }


                    if ( (input.LA(1) >= '0' && input.LA(1) <= '7') ) {
                        input.consume();
                    }
                    else {
                        MismatchedSetException mse = new MismatchedSetException(null,input);
                        recover(mse);
                        throw mse;
                    }


                    if ( (input.LA(1) >= '0' && input.LA(1) <= '7') ) {
                        input.consume();
                    }
                    else {
                        MismatchedSetException mse = new MismatchedSetException(null,input);
                        recover(mse);
                        throw mse;
                    }


                    }
                    break;
                case 2 :
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:530:9: '\\\\' ( '0' .. '7' ) ( '0' .. '7' )
                    {
                    match('\\'); 

                    if ( (input.LA(1) >= '0' && input.LA(1) <= '7') ) {
                        input.consume();
                    }
                    else {
                        MismatchedSetException mse = new MismatchedSetException(null,input);
                        recover(mse);
                        throw mse;
                    }


                    if ( (input.LA(1) >= '0' && input.LA(1) <= '7') ) {
                        input.consume();
                    }
                    else {
                        MismatchedSetException mse = new MismatchedSetException(null,input);
                        recover(mse);
                        throw mse;
                    }


                    }
                    break;
                case 3 :
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:531:9: '\\\\' ( '0' .. '7' )
                    {
                    match('\\'); 

                    if ( (input.LA(1) >= '0' && input.LA(1) <= '7') ) {
                        input.consume();
                    }
                    else {
                        MismatchedSetException mse = new MismatchedSetException(null,input);
                        recover(mse);
                        throw mse;
                    }


                    }
                    break;

            }

        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "OctalEscape"

    // $ANTLR start "UnicodeEscape"
    public final void mUnicodeEscape() throws RecognitionException {
        try {
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:536:5: ( '\\\\' 'u' HexDigit HexDigit HexDigit HexDigit )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:536:9: '\\\\' 'u' HexDigit HexDigit HexDigit HexDigit
            {
            match('\\'); 

            match('u'); 

            mHexDigit(); 


            mHexDigit(); 


            mHexDigit(); 


            mHexDigit(); 


            }


        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "UnicodeEscape"

    // $ANTLR start "WS"
    public final void mWS() throws RecognitionException {
        try {
            int _type = WS;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:538:5: ( ( ' ' | '\\r' | '\\t' | '\\u000C' | '\\n' ) )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:538:8: ( ' ' | '\\r' | '\\t' | '\\u000C' | '\\n' )
            {
            if ( (input.LA(1) >= '\t' && input.LA(1) <= '\n')||(input.LA(1) >= '\f' && input.LA(1) <= '\r')||input.LA(1)==' ' ) {
                input.consume();
            }
            else {
                MismatchedSetException mse = new MismatchedSetException(null,input);
                recover(mse);
                throw mse;
            }


            _channel=HIDDEN;

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "WS"

    // $ANTLR start "COMMENT"
    public final void mCOMMENT() throws RecognitionException {
        try {
            int _type = COMMENT;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:542:5: ( '/*' ( options {greedy=false; } : . )* '*/' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:542:9: '/*' ( options {greedy=false; } : . )* '*/'
            {
            match("/*"); 



            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:542:14: ( options {greedy=false; } : . )*
            loop30:
            do {
                int alt30=2;
                int LA30_0 = input.LA(1);

                if ( (LA30_0=='*') ) {
                    int LA30_1 = input.LA(2);

                    if ( (LA30_1=='/') ) {
                        alt30=2;
                    }
                    else if ( ((LA30_1 >= '\u0000' && LA30_1 <= '.')||(LA30_1 >= '0' && LA30_1 <= '\uFFFF')) ) {
                        alt30=1;
                    }


                }
                else if ( ((LA30_0 >= '\u0000' && LA30_0 <= ')')||(LA30_0 >= '+' && LA30_0 <= '\uFFFF')) ) {
                    alt30=1;
                }


                switch (alt30) {
            	case 1 :
            	    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:542:42: .
            	    {
            	    matchAny(); 

            	    }
            	    break;

            	default :
            	    break loop30;
                }
            } while (true);


            match("*/"); 



            _channel=HIDDEN;

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "COMMENT"

    // $ANTLR start "LINE_COMMENT"
    public final void mLINE_COMMENT() throws RecognitionException {
        try {
            int _type = LINE_COMMENT;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:546:5: ( '//' (~ ( '\\n' | '\\r' ) )* ( '\\r' )? '\\n' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:546:7: '//' (~ ( '\\n' | '\\r' ) )* ( '\\r' )? '\\n'
            {
            match("//"); 



            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:546:12: (~ ( '\\n' | '\\r' ) )*
            loop31:
            do {
                int alt31=2;
                int LA31_0 = input.LA(1);

                if ( ((LA31_0 >= '\u0000' && LA31_0 <= '\t')||(LA31_0 >= '\u000B' && LA31_0 <= '\f')||(LA31_0 >= '\u000E' && LA31_0 <= '\uFFFF')) ) {
                    alt31=1;
                }


                switch (alt31) {
            	case 1 :
            	    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:
            	    {
            	    if ( (input.LA(1) >= '\u0000' && input.LA(1) <= '\t')||(input.LA(1) >= '\u000B' && input.LA(1) <= '\f')||(input.LA(1) >= '\u000E' && input.LA(1) <= '\uFFFF') ) {
            	        input.consume();
            	    }
            	    else {
            	        MismatchedSetException mse = new MismatchedSetException(null,input);
            	        recover(mse);
            	        throw mse;
            	    }


            	    }
            	    break;

            	default :
            	    break loop31;
                }
            } while (true);


            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:546:26: ( '\\r' )?
            int alt32=2;
            int LA32_0 = input.LA(1);

            if ( (LA32_0=='\r') ) {
                alt32=1;
            }
            switch (alt32) {
                case 1 :
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:546:26: '\\r'
                    {
                    match('\r'); 

                    }
                    break;

            }


            match('\n'); 

            _channel=HIDDEN;

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "LINE_COMMENT"

    // $ANTLR start "LINE_COMMAND"
    public final void mLINE_COMMAND() throws RecognitionException {
        try {
            int _type = LINE_COMMAND;
            int _channel = DEFAULT_TOKEN_CHANNEL;
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:551:5: ( '#' (~ ( '\\n' | '\\r' ) )* ( '\\r' )? '\\n' )
            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:551:7: '#' (~ ( '\\n' | '\\r' ) )* ( '\\r' )? '\\n'
            {
            match('#'); 

            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:551:11: (~ ( '\\n' | '\\r' ) )*
            loop33:
            do {
                int alt33=2;
                int LA33_0 = input.LA(1);

                if ( ((LA33_0 >= '\u0000' && LA33_0 <= '\t')||(LA33_0 >= '\u000B' && LA33_0 <= '\f')||(LA33_0 >= '\u000E' && LA33_0 <= '\uFFFF')) ) {
                    alt33=1;
                }


                switch (alt33) {
            	case 1 :
            	    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:
            	    {
            	    if ( (input.LA(1) >= '\u0000' && input.LA(1) <= '\t')||(input.LA(1) >= '\u000B' && input.LA(1) <= '\f')||(input.LA(1) >= '\u000E' && input.LA(1) <= '\uFFFF') ) {
            	        input.consume();
            	    }
            	    else {
            	        MismatchedSetException mse = new MismatchedSetException(null,input);
            	        recover(mse);
            	        throw mse;
            	    }


            	    }
            	    break;

            	default :
            	    break loop33;
                }
            } while (true);


            // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:551:25: ( '\\r' )?
            int alt34=2;
            int LA34_0 = input.LA(1);

            if ( (LA34_0=='\r') ) {
                alt34=1;
            }
            switch (alt34) {
                case 1 :
                    // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:551:25: '\\r'
                    {
                    match('\r'); 

                    }
                    break;

            }


            match('\n'); 

            _channel=HIDDEN;

            }

            state.type = _type;
            state.channel = _channel;
        }
        finally {
        	// do for sure before leaving
        }
    }
    // $ANTLR end "LINE_COMMAND"

    public void mTokens() throws RecognitionException {
        // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:8: ( T__23 | T__24 | T__25 | T__26 | T__27 | T__28 | T__29 | T__30 | T__31 | T__32 | T__33 | T__34 | T__35 | T__36 | T__37 | T__38 | T__39 | T__40 | T__41 | T__42 | T__43 | T__44 | T__45 | T__46 | T__47 | T__48 | T__49 | T__50 | T__51 | T__52 | T__53 | T__54 | T__55 | T__56 | T__57 | T__58 | T__59 | T__60 | T__61 | T__62 | T__63 | T__64 | T__65 | T__66 | T__67 | T__68 | T__69 | T__70 | T__71 | T__72 | T__73 | T__74 | T__75 | T__76 | T__77 | T__78 | T__79 | T__80 | T__81 | T__82 | T__83 | T__84 | T__85 | T__86 | T__87 | T__88 | T__89 | T__90 | T__91 | T__92 | T__93 | T__94 | T__95 | T__96 | T__97 | T__98 | T__99 | T__100 | IDENTIFIER | CHARACTER_LITERAL | STRING_LITERAL | HEX_LITERAL | DECIMAL_LITERAL | OCTAL_LITERAL | FLOATING_POINT_LITERAL | WS | COMMENT | LINE_COMMENT | LINE_COMMAND )
        int alt35=89;
        alt35 = dfa35.predict(input);
        switch (alt35) {
            case 1 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:10: T__23
                {
                mT__23(); 


                }
                break;
            case 2 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:16: T__24
                {
                mT__24(); 


                }
                break;
            case 3 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:22: T__25
                {
                mT__25(); 


                }
                break;
            case 4 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:28: T__26
                {
                mT__26(); 


                }
                break;
            case 5 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:34: T__27
                {
                mT__27(); 


                }
                break;
            case 6 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:40: T__28
                {
                mT__28(); 


                }
                break;
            case 7 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:46: T__29
                {
                mT__29(); 


                }
                break;
            case 8 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:52: T__30
                {
                mT__30(); 


                }
                break;
            case 9 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:58: T__31
                {
                mT__31(); 


                }
                break;
            case 10 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:64: T__32
                {
                mT__32(); 


                }
                break;
            case 11 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:70: T__33
                {
                mT__33(); 


                }
                break;
            case 12 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:76: T__34
                {
                mT__34(); 


                }
                break;
            case 13 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:82: T__35
                {
                mT__35(); 


                }
                break;
            case 14 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:88: T__36
                {
                mT__36(); 


                }
                break;
            case 15 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:94: T__37
                {
                mT__37(); 


                }
                break;
            case 16 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:100: T__38
                {
                mT__38(); 


                }
                break;
            case 17 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:106: T__39
                {
                mT__39(); 


                }
                break;
            case 18 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:112: T__40
                {
                mT__40(); 


                }
                break;
            case 19 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:118: T__41
                {
                mT__41(); 


                }
                break;
            case 20 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:124: T__42
                {
                mT__42(); 


                }
                break;
            case 21 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:130: T__43
                {
                mT__43(); 


                }
                break;
            case 22 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:136: T__44
                {
                mT__44(); 


                }
                break;
            case 23 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:142: T__45
                {
                mT__45(); 


                }
                break;
            case 24 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:148: T__46
                {
                mT__46(); 


                }
                break;
            case 25 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:154: T__47
                {
                mT__47(); 


                }
                break;
            case 26 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:160: T__48
                {
                mT__48(); 


                }
                break;
            case 27 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:166: T__49
                {
                mT__49(); 


                }
                break;
            case 28 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:172: T__50
                {
                mT__50(); 


                }
                break;
            case 29 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:178: T__51
                {
                mT__51(); 


                }
                break;
            case 30 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:184: T__52
                {
                mT__52(); 


                }
                break;
            case 31 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:190: T__53
                {
                mT__53(); 


                }
                break;
            case 32 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:196: T__54
                {
                mT__54(); 


                }
                break;
            case 33 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:202: T__55
                {
                mT__55(); 


                }
                break;
            case 34 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:208: T__56
                {
                mT__56(); 


                }
                break;
            case 35 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:214: T__57
                {
                mT__57(); 


                }
                break;
            case 36 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:220: T__58
                {
                mT__58(); 


                }
                break;
            case 37 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:226: T__59
                {
                mT__59(); 


                }
                break;
            case 38 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:232: T__60
                {
                mT__60(); 


                }
                break;
            case 39 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:238: T__61
                {
                mT__61(); 


                }
                break;
            case 40 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:244: T__62
                {
                mT__62(); 


                }
                break;
            case 41 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:250: T__63
                {
                mT__63(); 


                }
                break;
            case 42 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:256: T__64
                {
                mT__64(); 


                }
                break;
            case 43 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:262: T__65
                {
                mT__65(); 


                }
                break;
            case 44 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:268: T__66
                {
                mT__66(); 


                }
                break;
            case 45 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:274: T__67
                {
                mT__67(); 


                }
                break;
            case 46 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:280: T__68
                {
                mT__68(); 


                }
                break;
            case 47 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:286: T__69
                {
                mT__69(); 


                }
                break;
            case 48 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:292: T__70
                {
                mT__70(); 


                }
                break;
            case 49 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:298: T__71
                {
                mT__71(); 


                }
                break;
            case 50 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:304: T__72
                {
                mT__72(); 


                }
                break;
            case 51 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:310: T__73
                {
                mT__73(); 


                }
                break;
            case 52 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:316: T__74
                {
                mT__74(); 


                }
                break;
            case 53 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:322: T__75
                {
                mT__75(); 


                }
                break;
            case 54 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:328: T__76
                {
                mT__76(); 


                }
                break;
            case 55 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:334: T__77
                {
                mT__77(); 


                }
                break;
            case 56 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:340: T__78
                {
                mT__78(); 


                }
                break;
            case 57 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:346: T__79
                {
                mT__79(); 


                }
                break;
            case 58 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:352: T__80
                {
                mT__80(); 


                }
                break;
            case 59 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:358: T__81
                {
                mT__81(); 


                }
                break;
            case 60 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:364: T__82
                {
                mT__82(); 


                }
                break;
            case 61 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:370: T__83
                {
                mT__83(); 


                }
                break;
            case 62 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:376: T__84
                {
                mT__84(); 


                }
                break;
            case 63 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:382: T__85
                {
                mT__85(); 


                }
                break;
            case 64 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:388: T__86
                {
                mT__86(); 


                }
                break;
            case 65 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:394: T__87
                {
                mT__87(); 


                }
                break;
            case 66 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:400: T__88
                {
                mT__88(); 


                }
                break;
            case 67 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:406: T__89
                {
                mT__89(); 


                }
                break;
            case 68 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:412: T__90
                {
                mT__90(); 


                }
                break;
            case 69 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:418: T__91
                {
                mT__91(); 


                }
                break;
            case 70 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:424: T__92
                {
                mT__92(); 


                }
                break;
            case 71 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:430: T__93
                {
                mT__93(); 


                }
                break;
            case 72 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:436: T__94
                {
                mT__94(); 


                }
                break;
            case 73 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:442: T__95
                {
                mT__95(); 


                }
                break;
            case 74 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:448: T__96
                {
                mT__96(); 


                }
                break;
            case 75 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:454: T__97
                {
                mT__97(); 


                }
                break;
            case 76 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:460: T__98
                {
                mT__98(); 


                }
                break;
            case 77 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:466: T__99
                {
                mT__99(); 


                }
                break;
            case 78 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:472: T__100
                {
                mT__100(); 


                }
                break;
            case 79 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:479: IDENTIFIER
                {
                mIDENTIFIER(); 


                }
                break;
            case 80 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:490: CHARACTER_LITERAL
                {
                mCHARACTER_LITERAL(); 


                }
                break;
            case 81 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:508: STRING_LITERAL
                {
                mSTRING_LITERAL(); 


                }
                break;
            case 82 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:523: HEX_LITERAL
                {
                mHEX_LITERAL(); 


                }
                break;
            case 83 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:535: DECIMAL_LITERAL
                {
                mDECIMAL_LITERAL(); 


                }
                break;
            case 84 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:551: OCTAL_LITERAL
                {
                mOCTAL_LITERAL(); 


                }
                break;
            case 85 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:565: FLOATING_POINT_LITERAL
                {
                mFLOATING_POINT_LITERAL(); 


                }
                break;
            case 86 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:588: WS
                {
                mWS(); 


                }
                break;
            case 87 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:591: COMMENT
                {
                mCOMMENT(); 


                }
                break;
            case 88 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:599: LINE_COMMENT
                {
                mLINE_COMMENT(); 


                }
                break;
            case 89 :
                // C:\\Users\\Even\\Documents\\Skole\\kpro9\\source\\grammar\\C.g:1:612: LINE_COMMAND
                {
                mLINE_COMMAND(); 


                }
                break;

        }

    }


    protected DFA25 dfa25 = new DFA25(this);
    protected DFA35 dfa35 = new DFA35(this);
    static final String DFA25_eotS =
        "\7\uffff\1\10\2\uffff";
    static final String DFA25_eofS =
        "\12\uffff";
    static final String DFA25_minS =
        "\2\56\2\uffff\1\53\1\uffff\2\60\2\uffff";
    static final String DFA25_maxS =
        "\1\71\1\146\2\uffff\1\71\1\uffff\1\71\1\146\2\uffff";
    static final String DFA25_acceptS =
        "\2\uffff\1\2\1\1\1\uffff\1\4\2\uffff\2\3";
    static final String DFA25_specialS =
        "\12\uffff}>";
    static final String[] DFA25_transitionS = {
            "\1\2\1\uffff\12\1",
            "\1\3\1\uffff\12\1\12\uffff\1\5\1\4\1\5\35\uffff\1\5\1\4\1\5",
            "",
            "",
            "\1\6\1\uffff\1\6\2\uffff\12\7",
            "",
            "\12\7",
            "\12\7\12\uffff\1\11\1\uffff\1\11\35\uffff\1\11\1\uffff\1\11",
            "",
            ""
    };

    static final short[] DFA25_eot = DFA.unpackEncodedString(DFA25_eotS);
    static final short[] DFA25_eof = DFA.unpackEncodedString(DFA25_eofS);
    static final char[] DFA25_min = DFA.unpackEncodedStringToUnsignedChars(DFA25_minS);
    static final char[] DFA25_max = DFA.unpackEncodedStringToUnsignedChars(DFA25_maxS);
    static final short[] DFA25_accept = DFA.unpackEncodedString(DFA25_acceptS);
    static final short[] DFA25_special = DFA.unpackEncodedString(DFA25_specialS);
    static final short[][] DFA25_transition;

    static {
        int numStates = DFA25_transitionS.length;
        DFA25_transition = new short[numStates][];
        for (int i=0; i<numStates; i++) {
            DFA25_transition[i] = DFA.unpackEncodedString(DFA25_transitionS[i]);
        }
    }

    class DFA25 extends DFA {

        public DFA25(BaseRecognizer recognizer) {
            this.recognizer = recognizer;
            this.decisionNumber = 25;
            this.eot = DFA25_eot;
            this.eof = DFA25_eof;
            this.min = DFA25_min;
            this.max = DFA25_max;
            this.accept = DFA25_accept;
            this.special = DFA25_special;
            this.transition = DFA25_transition;
        }
        public String getDescription() {
            return "507:1: FLOATING_POINT_LITERAL : ( ( '0' .. '9' )+ '.' ( '0' .. '9' )* ( Exponent )? ( FloatTypeSuffix )? | '.' ( '0' .. '9' )+ ( Exponent )? ( FloatTypeSuffix )? | ( '0' .. '9' )+ Exponent ( FloatTypeSuffix )? | ( '0' .. '9' )+ ( Exponent )? FloatTypeSuffix );";
        }
    }
    static final String DFA35_eotS =
        "\1\uffff\1\60\1\62\1\65\2\uffff\1\67\1\72\1\uffff\1\76\1\100\1\105"+
        "\2\uffff\1\110\1\112\1\115\3\uffff\1\117\17\50\1\uffff\1\153\5\uffff"+
        "\2\155\31\uffff\1\161\5\uffff\1\163\3\uffff\6\50\1\173\6\50\1\u0082"+
        "\13\50\5\uffff\1\u0093\1\155\4\uffff\7\50\1\uffff\4\50\1\u00a0\1"+
        "\50\1\uffff\1\u00a2\17\50\1\uffff\1\u00b2\1\50\1\u00b4\1\u00b5\4"+
        "\50\1\u00ba\1\u00bb\2\50\1\uffff\1\u00be\1\uffff\1\u00bf\13\50\1"+
        "\u00cb\2\50\1\uffff\1\u00ce\2\uffff\1\u00cf\3\50\2\uffff\1\50\1"+
        "\u00d4\2\uffff\2\50\1\u00d7\6\50\1\u00de\1\50\1\uffff\1\50\1\u00e1"+
        "\2\uffff\2\50\1\u00e4\1\u00e5\1\uffff\1\50\1\u00e7\1\uffff\1\u00e8"+
        "\1\u00e9\1\u00ea\1\u00eb\1\u00ec\1\50\1\uffff\2\50\1\uffff\1\50"+
        "\1\u00f1\2\uffff\1\50\6\uffff\1\u00f3\2\50\1\u00f6\1\uffff\1\u00f7"+
        "\1\uffff\1\u00f8\1\u00f9\4\uffff";
    static final String DFA35_eofS =
        "\u00fa\uffff";
    static final String DFA35_minS =
        "\1\11\2\75\1\46\2\uffff\1\75\1\53\1\uffff\1\55\1\56\1\52\2\uffff"+
        "\1\74\2\75\3\uffff\1\75\1\165\1\162\1\141\1\145\2\154\1\157\1\146"+
        "\1\157\1\145\1\150\1\171\1\156\1\157\1\150\1\uffff\1\75\5\uffff"+
        "\2\56\31\uffff\1\75\5\uffff\1\75\3\uffff\1\164\1\145\1\163\1\141"+
        "\1\156\1\146\1\44\1\163\1\165\1\164\1\157\1\162\1\164\1\44\1\164"+
        "\1\156\1\147\1\157\1\147\1\141\1\151\1\160\3\151\5\uffff\2\56\4"+
        "\uffff\1\157\1\141\1\145\1\162\1\163\1\141\1\142\1\uffff\1\145\1"+
        "\155\1\145\1\141\1\44\1\157\1\uffff\1\44\1\147\1\151\1\165\1\162"+
        "\1\156\1\145\1\164\1\165\1\164\1\145\1\157\1\151\1\144\1\141\1\154"+
        "\1\uffff\1\44\1\153\2\44\1\164\1\151\1\165\1\154\2\44\1\162\1\164"+
        "\1\uffff\1\44\1\uffff\1\44\1\163\1\162\1\164\1\145\1\157\1\151\2"+
        "\143\1\144\1\156\1\147\1\44\1\164\1\145\1\uffff\1\44\2\uffff\1\44"+
        "\1\156\1\154\1\145\2\uffff\1\156\1\44\2\uffff\1\164\1\156\1\44\1"+
        "\144\1\146\1\143\1\164\1\150\1\145\1\44\1\156\1\uffff\1\151\1\44"+
        "\2\uffff\1\165\1\164\2\44\1\uffff\1\145\1\44\1\uffff\5\44\1\146"+
        "\1\uffff\1\145\1\154\1\uffff\1\145\1\44\2\uffff\1\162\6\uffff\1"+
        "\44\1\144\1\145\1\44\1\uffff\1\44\1\uffff\2\44\4\uffff";
    static final String DFA35_maxS =
        "\1\176\3\75\2\uffff\2\75\1\uffff\1\76\1\71\1\75\2\uffff\2\75\1\76"+
        "\3\uffff\1\75\1\165\1\162\2\157\1\170\2\157\1\156\1\157\1\145\1"+
        "\167\1\171\1\156\1\157\1\150\1\uffff\1\174\5\uffff\1\170\1\146\31"+
        "\uffff\1\75\5\uffff\1\75\3\uffff\1\164\1\145\1\163\1\141\1\156\1"+
        "\146\1\172\1\163\1\165\1\164\1\157\1\162\1\164\1\172\1\164\1\156"+
        "\1\164\1\157\1\172\1\162\1\151\1\160\1\163\1\154\1\151\5\uffff\2"+
        "\146\4\uffff\1\157\1\141\1\145\1\162\1\164\1\141\1\142\1\uffff\1"+
        "\145\1\155\1\145\1\141\1\172\1\157\1\uffff\1\172\1\147\1\151\1\165"+
        "\1\162\1\156\1\145\1\164\1\165\1\164\1\145\1\157\1\151\1\144\1\141"+
        "\1\154\1\uffff\1\172\1\153\2\172\1\164\1\151\1\165\1\154\2\172\1"+
        "\162\1\164\1\uffff\1\172\1\uffff\1\172\1\163\1\162\1\164\1\145\1"+
        "\157\1\151\2\143\1\144\1\156\1\147\1\172\1\164\1\145\1\uffff\1\172"+
        "\2\uffff\1\172\1\156\1\154\1\145\2\uffff\1\156\1\172\2\uffff\1\164"+
        "\1\156\1\172\1\144\1\146\1\143\1\164\1\150\1\145\1\172\1\156\1\uffff"+
        "\1\151\1\172\2\uffff\1\165\1\164\2\172\1\uffff\1\145\1\172\1\uffff"+
        "\5\172\1\146\1\uffff\1\145\1\154\1\uffff\1\145\1\172\2\uffff\1\162"+
        "\6\uffff\1\172\1\144\1\145\1\172\1\uffff\1\172\1\uffff\2\172\4\uffff";
    static final String DFA35_acceptS =
        "\4\uffff\1\10\1\11\2\uffff\1\17\3\uffff\1\30\1\31\3\uffff\1\44\1"+
        "\45\1\46\20\uffff\1\111\1\uffff\1\115\1\116\1\117\1\120\1\121\2"+
        "\uffff\1\126\1\131\1\2\1\1\1\4\1\3\1\5\1\7\1\6\1\13\1\12\1\15\1"+
        "\16\1\14\1\21\1\22\1\23\1\20\1\25\1\24\1\125\1\27\1\127\1\130\1"+
        "\26\1\uffff\1\35\1\32\1\37\1\36\1\41\1\uffff\1\40\1\50\1\47\31\uffff"+
        "\1\113\1\114\1\112\1\122\1\123\2\uffff\1\34\1\33\1\43\1\42\7\uffff"+
        "\1\60\6\uffff\1\70\20\uffff\1\124\14\uffff\1\66\1\uffff\1\71\17"+
        "\uffff\1\51\1\uffff\1\53\1\54\4\uffff\1\62\1\63\2\uffff\1\67\1\72"+
        "\13\uffff\1\106\2\uffff\1\52\1\55\4\uffff\1\65\2\uffff\1\75\6\uffff"+
        "\1\104\2\uffff\1\110\2\uffff\1\61\1\64\1\uffff\1\74\1\76\1\77\1"+
        "\100\1\101\1\102\4\uffff\1\57\1\uffff\1\103\2\uffff\1\56\1\73\1"+
        "\105\1\107";
    static final String DFA35_specialS =
        "\u00fa\uffff}>";
    static final String[] DFA35_transitionS = {
            "\2\55\1\uffff\2\55\22\uffff\1\55\1\1\1\52\1\56\1\50\1\2\1\3"+
            "\1\51\1\4\1\5\1\6\1\7\1\10\1\11\1\12\1\13\1\53\11\54\1\14\1"+
            "\15\1\16\1\17\1\20\1\21\1\uffff\32\50\1\22\1\uffff\1\23\1\24"+
            "\1\50\1\uffff\1\25\1\26\1\27\1\30\1\31\1\32\1\33\1\50\1\34\2"+
            "\50\1\35\5\50\1\36\1\37\1\40\1\41\1\42\1\43\3\50\1\44\1\45\1"+
            "\46\1\47",
            "\1\57",
            "\1\61",
            "\1\63\26\uffff\1\64",
            "",
            "",
            "\1\66",
            "\1\70\21\uffff\1\71",
            "",
            "\1\73\17\uffff\1\74\1\75",
            "\1\77\1\uffff\12\101",
            "\1\103\4\uffff\1\104\15\uffff\1\102",
            "",
            "",
            "\1\106\1\107",
            "\1\111",
            "\1\113\1\114",
            "",
            "",
            "",
            "\1\116",
            "\1\120",
            "\1\121",
            "\1\122\6\uffff\1\123\6\uffff\1\124",
            "\1\125\11\uffff\1\126",
            "\1\127\1\uffff\1\130\11\uffff\1\131",
            "\1\132\2\uffff\1\133",
            "\1\134",
            "\1\135\7\uffff\1\136",
            "\1\137",
            "\1\140",
            "\1\141\1\142\12\uffff\1\143\2\uffff\1\144",
            "\1\145",
            "\1\146",
            "\1\147",
            "\1\150",
            "",
            "\1\151\76\uffff\1\152",
            "",
            "",
            "",
            "",
            "",
            "\1\101\1\uffff\10\156\2\101\12\uffff\3\101\21\uffff\1\154\13"+
            "\uffff\3\101\21\uffff\1\154",
            "\1\101\1\uffff\12\157\12\uffff\3\101\35\uffff\3\101",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "\1\160",
            "",
            "",
            "",
            "",
            "",
            "\1\162",
            "",
            "",
            "",
            "\1\164",
            "\1\165",
            "\1\166",
            "\1\167",
            "\1\170",
            "\1\171",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\24"+
            "\50\1\172\5\50",
            "\1\174",
            "\1\175",
            "\1\176",
            "\1\177",
            "\1\u0080",
            "\1\u0081",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "\1\u0083",
            "\1\u0084",
            "\1\u0085\14\uffff\1\u0086",
            "\1\u0087",
            "\1\u0088\22\uffff\1\u0089",
            "\1\u008a\20\uffff\1\u008b",
            "\1\u008c",
            "\1\u008d",
            "\1\u008e\11\uffff\1\u008f",
            "\1\u0090\2\uffff\1\u0091",
            "\1\u0092",
            "",
            "",
            "",
            "",
            "",
            "\1\101\1\uffff\10\156\2\101\12\uffff\3\101\35\uffff\3\101",
            "\1\101\1\uffff\12\157\12\uffff\3\101\35\uffff\3\101",
            "",
            "",
            "",
            "",
            "\1\u0094",
            "\1\u0095",
            "\1\u0096",
            "\1\u0097",
            "\1\u0098\1\u0099",
            "\1\u009a",
            "\1\u009b",
            "",
            "\1\u009c",
            "\1\u009d",
            "\1\u009e",
            "\1\u009f",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "\1\u00a1",
            "",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "\1\u00a3",
            "\1\u00a4",
            "\1\u00a5",
            "\1\u00a6",
            "\1\u00a7",
            "\1\u00a8",
            "\1\u00a9",
            "\1\u00aa",
            "\1\u00ab",
            "\1\u00ac",
            "\1\u00ad",
            "\1\u00ae",
            "\1\u00af",
            "\1\u00b0",
            "\1\u00b1",
            "",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "\1\u00b3",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "\1\u00b6",
            "\1\u00b7",
            "\1\u00b8",
            "\1\u00b9",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "\1\u00bc",
            "\1\u00bd",
            "",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "\1\u00c0",
            "\1\u00c1",
            "\1\u00c2",
            "\1\u00c3",
            "\1\u00c4",
            "\1\u00c5",
            "\1\u00c6",
            "\1\u00c7",
            "\1\u00c8",
            "\1\u00c9",
            "\1\u00ca",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "\1\u00cc",
            "\1\u00cd",
            "",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "",
            "",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "\1\u00d0",
            "\1\u00d1",
            "\1\u00d2",
            "",
            "",
            "\1\u00d3",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "",
            "",
            "\1\u00d5",
            "\1\u00d6",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "\1\u00d8",
            "\1\u00d9",
            "\1\u00da",
            "\1\u00db",
            "\1\u00dc",
            "\1\u00dd",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "\1\u00df",
            "",
            "\1\u00e0",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "",
            "",
            "\1\u00e2",
            "\1\u00e3",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "",
            "\1\u00e6",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "\1\u00ed",
            "",
            "\1\u00ee",
            "\1\u00ef",
            "",
            "\1\u00f0",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "",
            "",
            "\1\u00f2",
            "",
            "",
            "",
            "",
            "",
            "",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "\1\u00f4",
            "\1\u00f5",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "\1\50\13\uffff\12\50\7\uffff\32\50\4\uffff\1\50\1\uffff\32"+
            "\50",
            "",
            "",
            "",
            ""
    };

    static final short[] DFA35_eot = DFA.unpackEncodedString(DFA35_eotS);
    static final short[] DFA35_eof = DFA.unpackEncodedString(DFA35_eofS);
    static final char[] DFA35_min = DFA.unpackEncodedStringToUnsignedChars(DFA35_minS);
    static final char[] DFA35_max = DFA.unpackEncodedStringToUnsignedChars(DFA35_maxS);
    static final short[] DFA35_accept = DFA.unpackEncodedString(DFA35_acceptS);
    static final short[] DFA35_special = DFA.unpackEncodedString(DFA35_specialS);
    static final short[][] DFA35_transition;

    static {
        int numStates = DFA35_transitionS.length;
        DFA35_transition = new short[numStates][];
        for (int i=0; i<numStates; i++) {
            DFA35_transition[i] = DFA.unpackEncodedString(DFA35_transitionS[i]);
        }
    }

    class DFA35 extends DFA {

        public DFA35(BaseRecognizer recognizer) {
            this.recognizer = recognizer;
            this.decisionNumber = 35;
            this.eot = DFA35_eot;
            this.eof = DFA35_eof;
            this.min = DFA35_min;
            this.max = DFA35_max;
            this.accept = DFA35_accept;
            this.special = DFA35_special;
            this.transition = DFA35_transition;
        }
        public String getDescription() {
            return "1:1: Tokens : ( T__23 | T__24 | T__25 | T__26 | T__27 | T__28 | T__29 | T__30 | T__31 | T__32 | T__33 | T__34 | T__35 | T__36 | T__37 | T__38 | T__39 | T__40 | T__41 | T__42 | T__43 | T__44 | T__45 | T__46 | T__47 | T__48 | T__49 | T__50 | T__51 | T__52 | T__53 | T__54 | T__55 | T__56 | T__57 | T__58 | T__59 | T__60 | T__61 | T__62 | T__63 | T__64 | T__65 | T__66 | T__67 | T__68 | T__69 | T__70 | T__71 | T__72 | T__73 | T__74 | T__75 | T__76 | T__77 | T__78 | T__79 | T__80 | T__81 | T__82 | T__83 | T__84 | T__85 | T__86 | T__87 | T__88 | T__89 | T__90 | T__91 | T__92 | T__93 | T__94 | T__95 | T__96 | T__97 | T__98 | T__99 | T__100 | IDENTIFIER | CHARACTER_LITERAL | STRING_LITERAL | HEX_LITERAL | DECIMAL_LITERAL | OCTAL_LITERAL | FLOATING_POINT_LITERAL | WS | COMMENT | LINE_COMMENT | LINE_COMMAND );";
        }
    }
 

}