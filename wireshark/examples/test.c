#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include "time.h"
#include "headers\agent.h"
#include "headers\xtypes.h"
#include "headers\sap.h"
#include "headers\huge.h"
#include "headers\xcon.h"


SAP init_sap(int i)
{
   SAP s;

   switch(i) {
   case 1:
      s.afi = 1;
      break;
   case 2:
      s.afi = 2;
      break;
   default:
      s.afi = 0xff;
      break;
   }

   return s;
}


/** todo */
TSK_ADDRESS init_tsk_address()
{
   TSK_ADDRESS t = {0};

   return t;
}


/** todo */
struct ctx init_ctx(int i)
{
   struct ctx s = {0};

   return s;
}


/** todo */
struct abc_p init_abc_p()
{
   struct abc_p s = {0};

   return s;
}


/** todo */
struct rst_p init_rst_p()
{
   struct rst_p s = {0};

   return s;
}


/** todo */
struct pl_p init_pl_p()
{
   struct pl_p s = {0};

   return s;
}


/** todo */
struct sl_p init_sl_p()
{
   struct sl_p s = {0};

   return s;
}


/** todo */
struct nl_p init_nl_p()
{
   struct nl_p s = {0};

   return s;
}


/** todo */
struct huge_t init_huge_t()
{
   struct huge_t h = {0};

   return h;
}


/** todo */
time_t init_time_t()
{
   time_t t = {0};

   return t;
}

/** todo */
nstime_t init_nstime_t()
{
   nstime_t t = {0};

   return t;
}

struct xcon *init_xcon()
{
   unsigned int i;
   const unsigned int NUM_CTX = 2;
   const unsigned int NUM_NLP = 3;
   const char *asn1_data = "\x30\x08\x81\x02\x08\x9e\x82\x02\x03\x04";
   /* Note: ASN.1 may contain \0, so this won't always work.. */
   const unsigned int ASN1_DATA_LEN = strlen(asn1_data);

   struct xcon *xc = malloc(sizeof(struct xcon)
		            + sizeof(struct ctx) * NUM_CTX
			    + sizeof(struct nl_p) * NUM_NLP
             + ASN1_DATA_LEN);
   struct ctx *ctxp = (struct ctx*)   (xc   + 1);
   struct nl_p *nlpp = (struct nl_p*) (ctxp + NUM_CTX);
   char* asn1p =              (char*) (nlpp + NUM_NLP);

   /* Could do this in one big memset, but wanted to show each section.. */
   memset(xc, 0, sizeof(struct xcon));
   memset(ctxp, 0, sizeof(struct ctx)*NUM_CTX);
   memset(nlpp, 0, sizeof(struct nl_p)*NUM_NLP);
   memset(asn1p, 0, ASN1_DATA_LEN);

   xc->agent_type = AGENT_D;
   xc->agent_id = 11233342;
   xc->features = 0x01 | 0x02 | 0x08 | 0x10;
   xc->pres_ctx[0] = 70000000;
   xc->pres_ctx[1] = 6000000;
   xc->pres_ctx[2] = 500000;
   xc->pres_ctx[4] = 3000;
   xc->pres_ctx[5] = 200;
   xc->pres_ctx[6] = 10;
   xc->pres_ctx[7] = 0;
   xc->common_ref[0] = 12;
   xc->common_ref[4] = 106;
   strcpy (xc->name, "CSjark uttales sæschjaschjjjk");
   xc->a_xsap = init_sap(1);
   xc->b_xsap = init_sap(2);
   xc->result_source = 22;
   xc->diagnostic = -23;
   xc->trak = 554;
   xc->link = init_tsk_address();
   xc->context = init_ctx(0);
   xc->abc = init_abc_p();
   xc->rst = init_rst_p();
   xc->pl  = init_pl_p();
   xc->sl  = init_sl_p();
   xc->nl  = init_nl_p();
   xc->gir = 64646464;
   xc->colour = GREEN;
   xc->fatso = init_huge_t();
   strcpy (xc->filename, "/path/to/file/buried/very/very/very/very/very/very/very/very/very/very/very/very/very/very/very/very/very/far/down");
   xc->created = init_nstime_t();
   xc->timeout = init_time_t();
   xc->ctx_no = NUM_CTX;
   xc->nlp_no = NUM_NLP;

   for (i = 0; i < NUM_CTX; i++) {
      ctxp[i] = init_ctx(i+1);
   }

   for (i = 0; i < NUM_NLP; i++) {
      nlpp[i] = init_nl_p(i);
   }

   memcpy(asn1p, asn1_data, ASN1_DATA_LEN);

   return xc;

}

void print_int_array(const char* prefix, const int *array, const size_t size)
{
   unsigned int i;

   printf("%s=[", prefix);
   if (size == 0) {
      printf("]\n");
      return;
   }

   printf("%d", array[0]);
   for(i = 0; i < size; i++) {
      printf(", %d", array[i]);
   }
   printf("]\n");
}

void print_octet_array(const char* prefix, const OCTET *array, const size_t size)
{
   unsigned int i;
   printf("%s=[", prefix);
   if (size == 0) {
      printf("]\n");
      return;
   }

   printf("%c", array[0]);
   for(i = 0; i < size; i++) {
      printf(", %c", array[i]);
   }
   printf("]\n");
}

void print_char_array(const char* prefix, const char *array, const size_t size)
{
   unsigned int i;
   printf("%s=[", prefix);
   if (size == 0) {
      printf("]\n");
      return;
   }

   printf("%c", array[0]);
   for(i = 0; i < size; i++) {
      printf(", %hhd", array[i]);
   }
   printf("]\n");
}

void print_sap(const char* prefix, const SAP *sap)
{
   printf("%s=TODO\n", prefix);
}


void print_xcon(struct xcon *xc)
{
   printf("agent_type=%d\n", xc->agent_type);
   printf("agent_id=%lu\n", xc->agent_id);
   printf("features=0x%x\n", xc->features);
   print_int_array("pres_ctx", xc->pres_ctx, sizeof(xc->pres_ctx)/sizeof(int));
   print_octet_array("common_ref", xc->common_ref, sizeof(xc->common_ref)/sizeof(OCTET));
   printf("name=%s\n", xc->name);
   print_sap("a_xsap=", &xc->a_xsap);
   print_sap("b_xsap=", &xc->b_xsap);
   printf("result_source=%d\n", xc->result_source);
   printf("diagnostic=%d\n", xc->diagnostic);
}

int main(int argc, char *argv[])
{
   struct xcon *xc;

   xc = init_xcon();

   print_xcon(xc);

}

