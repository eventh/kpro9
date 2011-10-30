#ifndef SAP_H
#define SAP_H

#define DSP_LEN 10

typedef OCTET AFI;
typedef OCTET IDI[10];
typedef OCTET DSP[DSP_LEN+1];

#define AFI_OLD 0
#define AFI_A   1
#define AFI_B   2
#define AFI_C   3

typedef struct {
   union {
      struct {
         AFI       afi;
         IDI       idi;
      } _SAP_old;

      /*
      ** The following structure should be used if AFI == A
      */
      struct {
         AFI     s_afi;
         char    s_hoe[10 + DSP_LEN - 1];
         /*
         ** Note: s_port should have been a short, but is located in
         ** an unaligned address in _SAP_old. For compatibility reasons,
         ** we therefore still use two characters
         */
         char    s_port[2];
      } _SAP_a;

      /*
      ** The following structure should be used if AFI == B
      */
      struct {
         AFI       s_afi;
         uint32_t  s_rawp;
         short     s_rapo;
      } _SAP_b;

#ifdef VV6
      /*
      ** The following structure should be used if AFI == C
      */
      struct {
         AFI        s_afi;
         uint32_t   s_net;
         uint32_t   s_sk;
      } _SAP_c;
#endif

   } _SAP_un;

   /* Define macros to maintain backwards source compatibility */
#define afi        _SAP_un._SAP_old.afi
#define idi        _SAP_un._SAP_old.idi
#define sap_hoe    _SAP_un._SAP_a.s_hoe
#define sap_port   _SAP_un._SAP_a.s_port
#define sap_rawp   _SAP_un._SAP_b.s_rawp
#define sap_rapo   _SAP_un._SAP_b.s_rapo

#ifdef VV6
#define sap_net    _SAP_un._SAP_c.s_net
#define sap_sk     _SAP_un._SAP_c.s_sk
#endif

} SAP;

#endif
