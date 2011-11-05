/*
** Some internally defined types.
*/

#ifndef XTYPES_H
#define XTYPES_H

#if HAVE_PRAGMA_IDENT
#pragma ident "@(#) $Id$"
#endif

#include <time.h>

/* MAX_PATH */
#ifdef LINUX
#include <linux/limits.h>
#else
#include <limits.h>
#endif

#ifdef _WIN32
#define WIN32
#endif

#ifdef WIN32
   /*
   ** Windows does not define size_t in sys/types.h
   */
#ifndef _KERNEL
#include <windows.h>
#include <windef.h>
#include <stddef.h>
#include <errno.h>
#endif

#ifndef NDEBUG
   /* Disable STL-warnings.... */
#pragma warning(disable : 4786)
#endif

#endif /* WIN32 */

/* Maximum length for file paths.                */
/* Unix uses PATH_MAX. In Windows, use MAX_PATH. */
#ifdef WIN32
#define PATH_MAX MAX_PATH
#endif

#if defined(WIN32) || defined(LINUX) || defined(__APPLE__)
// TODO: Already defined!
//typedef unsigned long long  uint64_t;
//typedef unsigned int  uint32_t;
//typedef unsigned char uint8_t;
#endif

#ifdef WIN32
typedef int BOOL;
#else
typedef unsigned char BOOL;
#endif

#ifndef FALSE
#define FALSE 0
#define TRUE 1
#endif

typedef  int            ALIGN;
typedef  unsigned char  OCTET;
typedef  unsigned short WORD;

typedef short           TSK_INST;
typedef short           TSK_PREF;
typedef short           TSK_MSG;
typedef int		TSK_TRAK;

typedef  struct tsk_address {
   TSK_PREF       pref;
   TSK_INST       inst;
   short          que_id;
} TSK_ADDRESS;

/* Time definition for absolute time */
typedef struct {
   time_t  secs;
   int     nsecs;
} nstime_t;

enum colour_t {
	RED,
	ORANGE,
	YELLOW,
	GREEN,
	BLUE,
	INDIGO,
	VIOLET
};

#ifndef MAXUCHAR
#define MAXUCHAR    UCHAR_MAX
#endif
#ifndef MAXUSHORT
#define MAXUSHORT   USHRT_MAX
#endif
#ifndef MAXINT
#define MAXINT      INT_MAX
#endif
#ifndef MAXUINT
#define MAXUINT     UINT_MAX
#endif
#ifndef MAXULONG
#define MAXULONG    ULONG_MAX
#endif

#ifndef MININT
#ifdef WIN32
#define MININT      INT_MIN
#else
#define MININT      (-MAXINT-1) /* Assumes two's complement */
#endif
#endif

#ifdef WIN32                               /* avoid conflict with winnt.h */
#ifndef MAXCHAR
#define MAXCHAR     0x7f
#endif
#ifndef MAXSHORT
#define MAXSHORT    0x7fff
#endif
#ifndef MAXLONG
#define MAXLONG     0x7fffffff
#endif
#else
#define MAXCHAR     CHAR_MAX
#define MAXSHORT    SHRT_MAX
#define MAXLONG     LONG_MAX
#endif /* WIN32 */

#endif /* XTYPES_H */
