/****************************************************************************************
 * @file       block_functions.h
 * @brief      Kratak opis block_functions.h
 * @details    Detaljan opis
 * @author     vujanovic
 * @version    1.0
 * @date       Dec 25, 2014
 * @pre        -
 * @bug        -
 * @warning    -
 ****************************************************************************************/
#ifndef __block_functions_h__
#define __block_functions_h__

#ifdef __cplusplus
extern "C"
{
#endif /* __cplusplus */

/*------------------------------------------------------------------------------
 DEFINES
 ------------------------------------------------------------------------------*/

/*------------------------------------------------------------------------------
 ENUMS
 ------------------------------------------------------------------------------*/

/*------------------------------------------------------------------------------
 TYPEDEFS
 ------------------------------------------------------------------------------*/

/*------------------------------------------------------------------------------
 FUNCTIONS
 ------------------------------------------------------------------------------*/

/*-----------------------------------------------------------------------------------*/
/**
 * @brief   Funkcija \c read kojom se implementira funkcinalnost bloka "ulaz"
 */
float ulaz(void);

/*-----------------------------------------------------------------------------------*/
/**
 * @brief   Funkcija \c sin implementira funkcionalnost za blok "sinus"
 */
float sinus(float in);

/*-----------------------------------------------------------------------------------*/
/**
 * @brief   Funkcija \c cos implementira dunkcionalnost bloka sa tipa "kosinus"
 */
float kosinus(float in);

/*-----------------------------------------------------------------------------------*/
/**
 * @brief   Funkcija \c sqrt implementira funkcionalnost za blok "kvkoren"
 */
float kvkoren(float in);

/*-----------------------------------------------------------------------------------*/
/**
 * @brief   Funkcija \c print implenentira blok "izlaz"
 */
void izlaz(float in);


#ifdef __cplusplus
}
#endif /*__cplusplus */
#endif /* __block_functions_h__ */
