/*
** Defines used to define struct xcon.
*/

#ifndef XCON_H
#define XCON_H

#if HAVE_PRAGMA_IDENT
#pragma ident "@(#) $Id$"
#endif

#include <time.h>

/*
** Machine-dependent types
*/
#ifndef _NETDLC_UINT_H
typedef  unsigned char  uint8;
typedef  unsigned short uint16;
typedef  unsigned long  uint32;
#endif
typedef  char           sint8;
typedef  short          sint16;
typedef  long           sint32;

/*
** Application contexts
*/
#define MSS                          0    /* MSS Context                */
#define DIR_ACCESS_PROT             12    /* Directory App Context      */
#define DIR_SYSTEM_PROT             13    /* Directory System Context   */
#define DROP_BIND_MGMT              15    /* DROP                       */
#define DIR_CUST_INIT               16    /* DISP, customer initiated   */
#define DIR_SUPP_INIT               17    /* DISP, supplier initiated   */
#define HIGHEST_AC                  20 /* Note: Uses value as "unknown AC" */

#define CTX_LIST_LEN  8      


#define NEGATIVE     FALSE
#define AFFIRMATIVE ~NEGATIVE

typedef int DIAGNOSTIC;
typedef int RESULT_SOURCE;


#ifdef MODULE_TEST
#define CALL_REF_LEN     1
#define COM_REF_LEN      1
#define ADD_REF_LEN      1
#define USER_DATA_LEN    1
#define SPT_PRI_LEN      1
#else
#define CALL_REF_LEN    64
#define COM_REF_LEN     64
#define ADD_REF_LEN      4
#define USER_DATA_LEN    9
#define SPT_PRI_LEN      4
#endif


/*
** ABC parameters 
*/
struct abc_p {                                                               
   uint8          foo;
   uint8          bar;
   uint8          baz;
   uint8          fuzz;
   uint8          kluss;
   uint8          sjasjke;
   uint8          dooooooooiiiioooiii;
   unsigned short green;
   unsigned short waffles;
   unsigned short levers;
   unsigned short lasers;
   int            a;
   unsigned long long ultralong;
};

/*
** RST parameters
*/
struct rst_p {
   uint8          tok_sz;               /* rst token size                    */
   uint8          hkp_sz;               /* rst HKP size                      */
   unsigned int   d_mode;               /* rst detail mode                   */
   unsigned int   initial_turn;         /*                                   */
   unsigned long  recover_timer;        /*                                   */
};

/* Initial turn values */
#define INITIATOR    0
#define RESPONDER    1


/*
** PL parameters
*/
struct pl_p {                                                                
   uint8          protver;              /* def 1                             */
   unsigned int   req;                  /* functional unit, def PL_KERNEL    */
};

/* PL functional units */
#define PL_KERNEL       0
#define PL_USER         1
#define PL_MODE         2


/*
** SL parameters 
*/
struct sl_p {                                                                
   uint8          protver;              /* def 1                             */
   BOOL           ext_concat;           /* def FALSE                         */
   BOOL           ext_cntrl;            /* def FALSE                         */
   BOOL           opt_dial;             /* def FALSE                         */
   unsigned int   rel_token;            /* def TOK_AAA                       */
   unsigned int   act_token;            /* def TOK_AAA                       */
   unsigned int   minsync_token;        /* def TOK_AAA                       */
   unsigned int   data_token;           /* def TOK_AAA                       */
   unsigned short req;                  /* functional units, def MBAS_FU     */
   unsigned long  max_tsdu_sz_out;      /* def 0 (no limit)                  */
   unsigned long  max_tsdu_sz_in;       /* def 0 (no limit)                  */
};

/* SL fu */
#define SL_FU_HD           0x001
#define SL_FU_FD           0x002
#define SL_FU_EX           0x004
#define SL_FU_SY           0x008
#define SL_FU_MA           0x010
#define SL_FU_RESYN        0x020
#define SL_FU_ACT          0x040
#define SL_FU_NR           0x080
#define SL_FU_CD           0x100
#define SL_FU_EXCEP        0x200
#define SL_FU_TD           0x400

/* SL functional subsets */
#define MBAS_FU            (0x249) /* K | HD | SY | EXCEP | ACT */
#define BAS_FU             (0x749) /* K | HD | TD | CD | SY | EXCEP | ACT */
#define BSS_FU             (0x4bb) /* K | NR | HD | FD | TD | SY | MA */
#define BCS_FU             (0x003) /* K | HD | FD */

/* SL tokens */
#define TOK_AAA 1
#define TOK_BBB 2
#define TOK_CCC 3

/*
** NL parameters.
*/

#define GNRL_AEF_LEN  40        /* Ref. std. */

#define CU_DTA_LEN   128

#define SRC_RT_LEN     4

struct gnrl_aef {                    /* General AEF data                   */
   unsigned char  aef_len;           /* Length of AEF, 0 if none           */
   OCTET          aef[GNRL_AEF_LEN]; /* The AEF data                       */
};

                                   
struct src_rt {                    
   unsigned char  no_idi;          
   IDI            sr_idi[SRC_RT_LEN]; /* Each IDI with length field set      */
};   


/* aef_type defines, note that these are mutually exclusive */
#define AEF_GNRL    1          /* Gen AEF data */
#define AEF_SRC_RT  2          /* Spath */

struct adr_ext {
   unsigned char      aef_type;  /* AEF type, defines above, 0 if no AEF     */
   union {
      struct gnrl_aef aef;       /* The AEF data                      */
      struct src_rt   src_rt;
   } uaef;
};


struct nl_p {
   BOOL           exp_dta;       /* Expedited data, FALSE=none               */
   BOOL           rec_conf;      /* Receipt req.    FALSE=none               */
   unsigned short pvc_no;        /* pvc_no == 0 means VC, else PVC           */
   unsigned char  fs_rfs;     /* 0: Not requested
                                 1: No restrictions
                                 2: Restrictions on response
                                 3: Reduced mode */

   struct adr_ext cld_aef;       /* Called ext facility */
   struct adr_ext clg_aef;       /* Calling ext facility */

   OCTET          cu_dta[CU_DTA_LEN];  /* 0-128 octets */
   BOOL           use_ip_pri;    /* Use precedence bit */
};

/*
** Address format definitions
*/
#define AF_BINARY_ADDR  0x8000   /* Raw IP address / subnet etc */
#define AF_APS_ADDR     0x4000   /* APS address */
#define AF_LAN_ADDR     0x2000   /* LAN address */

struct ctx {
   int               appl_ctx;                /* application context */
   int               pres_ctx[CTX_LIST_LEN];  /* presentation context */
   OCTET             common_ref[COM_REF_LEN];
};

/* GIR flags */
#define GIR_FLAG_ACTIVE     0x0001         /* State enabled/disabled */
#define GIR_FLAG_GREEN      0x0002         /* Good?                  */
#define GIR_FLAG_SENDING    0x0004         /* May send data          */
#define GIR_FLAG_RCVING     0x0008         /* May receive data       */
#define GIR_FLAG_DUPLEX     0x0010
#define GIR_FLAG_BIGENDIAN  0x0100
#define GIR_FLAG_MD5        0x0200
#define GIR_FLAG_SHA128     0x0400
#define GIR_FLAG_SHA256     0x0800
#define GIR_FLAG_RESERVED1  0x1000
#define GIR_FLAG_RESERVED2  0x2000
#define GIR_FLAG_RESERVED3  0x4000
#define GIR_FLAG_RESERVED4  0x8000

/* */

struct xcon {                               /* x = a,p or s*/
   AGENT_TYPE        agent_type;	 /* typedef of standard type */
   unsigned long     agent_id;		 /* standard type */
   unsigned char     features;           /* std type */
   int               pres_ctx[CTX_LIST_LEN+1];  /* int array + addition */
   OCTET             common_ref[COM_REF_LEN]; /* typedeffed array */
   char              name[50];		 /* C-string                       */
   SAP               a_xsap;		 /* struct with union+structs in it */
   SAP               b_xsap;		 /* struct with union+structs in it */
   RESULT_SOURCE     result_source;      /* typedef of std type            */
   DIAGNOSTIC        diagnostic;         /* typedef of std type            */
   TSK_TRAK          trak;               /* typedef of std type            */
   TSK_ADDRESS       link;               /* struct with typedef members    */
   struct ctx        context;            /* Struct with arrays as members  */
   struct abc_p      abc;                /* long struct                    */
   struct rst_p      rst;                /* rst parameters                 */
   struct pl_p       pl;                 /* pl parameters                  */
   struct sl_p       sl;                 /* sl parameters                  */
   struct nl_p       nl;
   unsigned int      gir;                /* gir bitmask                    */
   int               limited;            /* min -200, max 200              */
   enum colour_t     colour;             /* enum with color names          */
   struct huge_t     fatso;              /* struct with 200 members        */
   char              filename[PATH_MAX]; /* Use system definition          */
   nstime_t          created;            /* Creation time (absolute time)  */
   time_t            timeout;            /* seconds to timeout (relative)  */
   int               ctx_no;             /* number of ctx structs following */
   int               nlp_no;             /* number of nl_p structs following */
};
  /* User data follows as ASN.1 */

#endif /* XCON_H */
