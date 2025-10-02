import pandas as pd
import os

def analizar_pilotos_especificos(tabla_historica, results, races, drivers):
    """
    Análisis histórico detallado de Sergio Pérez y Valtteri Bottas
    """
    print("\n" + "="*80)
    print("🔍 ANÁLISIS HISTÓRICO DETALLADO DE PILOTOS ESPECÍFICOS")
    print("="*80)
    
    # Buscar los IDs de los pilotos
    perez_id = drivers[drivers['surname'] == 'Pérez']['driverId'].iloc[0]
    bottas_id = drivers[drivers['surname'] == 'Bottas']['driverId'].iloc[0]
    
    # Función auxiliar para analizar un piloto
    def analizar_piloto(driver_id, nombre_piloto):
        print(f"\n🏎️  {nombre_piloto.upper()}")
        print("-" * 50)
        
        # Datos básicos del piloto
        piloto_info = drivers[drivers['driverId'] == driver_id].iloc[0]
        datos_tabla = tabla_historica[tabla_historica['Código'] == piloto_info['driverRef']].iloc[0]
        
        print(f"📊 ESTADÍSTICAS GENERALES:")
        print(f"   • Nombre completo: {piloto_info['forename']} {piloto_info['surname']}")
        print(f"   • Nacionalidad: {piloto_info['nationality']}")
        print(f"   • Fecha de nacimiento: {piloto_info['dob']}")
        print(f"   • Puntos totales carrera: {datos_tabla['Puntos Totales']:,.1f}")
        print(f"   • Carreras disputadas: {datos_tabla['Carreras']}")
        print(f"   • Victorias: {int(datos_tabla['Victorias'])}")
        print(f"   • Promedio puntos/carrera: {datos_tabla['Puntos/Carrera']}")
        
        # Análisis por temporadas
        resultados_piloto = results[results['driverId'] == driver_id].copy()
        resultados_con_carreras = resultados_piloto.merge(races[['raceId', 'year', 'name']], on='raceId')
        
        # Estadísticas por año
        stats_por_año = resultados_con_carreras.groupby('year').agg({
            'points': 'sum',
            'raceId': 'count',
            'position': lambda x: sum(1 for pos in x if pos == '1')  # Victorias
        }).reset_index()
        stats_por_año.columns = ['Año', 'Puntos', 'Carreras', 'Victorias']
        
        print(f"\n📈 EVOLUCIÓN POR TEMPORADAS:")
        # Mostrar solo años con carreras
        stats_filtrado = stats_por_año[stats_por_año['Carreras'] > 0].sort_values('Año', ascending=False)
        for _, row in stats_filtrado.head(10).iterrows():
            print(f"   {int(row['Año'])}: {row['Puntos']:6.1f} puntos, {int(row['Carreras']):2d} carreras, {int(row['Victorias']):2d} victorias")
        
        # Mejores temporadas
        mejor_temporada = stats_filtrado.loc[stats_filtrado['Puntos'].idxmax()]
        print(f"\n🏆 MEJOR TEMPORADA: {int(mejor_temporada['Año'])} ({mejor_temporada['Puntos']:.1f} puntos)")
        
        # Análisis de podios
        podios = resultados_con_carreras[
            (resultados_con_carreras['position'].isin(['1', '2', '3'])) & 
            (resultados_con_carreras['position'] != '\\N')
        ]
        total_podios = len(podios)
        
        if total_podios > 0:
            print(f"🥇 PODIOS: {total_podios} totales")
            podios_por_pos = podios['position'].value_counts().sort_index()
            for pos, count in podios_por_pos.items():
                pos_names = {'1': '1° lugar', '2': '2° lugar', '3': '3° lugar'}
                print(f"   • {pos_names[pos]}: {count}")
        
        # Circuitos favoritos (más puntos)
        puntos_por_circuito = resultados_con_carreras.groupby('name')['points'].sum().sort_values(ascending=False)
        print(f"\n🏁 TOP 3 CIRCUITOS (más puntos):")
        for i, (circuito, puntos) in enumerate(puntos_por_circuito.head(3).items(), 1):
            print(f"   {i}. {circuito}: {puntos:.1f} puntos")
        
        # Racha de puntos
        resultados_ordenados = resultados_con_carreras.sort_values(['year', 'raceId'])
        resultados_ordenados['puntos_conseguidos'] = resultados_ordenados['points'] > 0
        
        # Calcular racha actual
        racha_actual = 0
        for puntos in reversed(resultados_ordenados['puntos_conseguidos'].tolist()):
            if puntos:
                racha_actual += 1
            else:
                break
        
        if racha_actual > 0:
            print(f"\n⚡ RACHA ACTUAL: {racha_actual} carreras consecutivas sumando puntos")
        
        return stats_por_año
    
    # Analizar ambos pilotos
    stats_perez = analizar_piloto(perez_id, "SERGIO PÉREZ")
    stats_bottas = analizar_piloto(bottas_id, "VALTTERI BOTTAS")
    
    # Comparación directa
    print(f"\n⚖️  COMPARACIÓN DIRECTA")
    print("-" * 50)
    
    perez_datos = tabla_historica[tabla_historica['Código'] == 'perez'].iloc[0]
    bottas_datos = tabla_historica[tabla_historica['Código'] == 'bottas'].iloc[0]
    
    print(f"Puntos totales:")
    print(f"   • Pérez: {perez_datos['Puntos Totales']:,.1f}")
    print(f"   • Bottas: {bottas_datos['Puntos Totales']:,.1f}")
    print(f"   • Diferencia: {abs(perez_datos['Puntos Totales'] - bottas_datos['Puntos Totales']):.1f} puntos")
    
    print(f"\nVictorias:")
    print(f"   • Pérez: {int(perez_datos['Victorias'])}")
    print(f"   • Bottas: {int(bottas_datos['Victorias'])}")
    
    print(f"\nPromedio puntos/carrera:")
    print(f"   • Pérez: {perez_datos['Puntos/Carrera']:.2f}")
    print(f"   • Bottas: {bottas_datos['Puntos/Carrera']:.2f}")
    
    # Posiciones en el ranking histórico
    pos_perez = tabla_historica[tabla_historica['Código'] == 'perez'].index[0] + 1
    pos_bottas = tabla_historica[tabla_historica['Código'] == 'bottas'].index[0] + 1
    
    print(f"\nPosición en ranking histórico:")
    print(f"   • Pérez: #{pos_perez}")
    print(f"   • Bottas: #{pos_bottas}")

def crear_tabla_historica_pilotos():
    """
    Crea una tabla histórica de pilotos basada en los puntos totales sumados 
    a lo largo de toda su carrera en la Fórmula 1
    """
    ruta = "../archive/"
    
    print("📊 Creando tabla histórica de pilotos...")
    
    # Cargar los datos necesarios
    print("📂 Cargando datos...")
    drivers = pd.read_csv(ruta + "drivers.csv")
    results = pd.read_csv(ruta + "results.csv")
    races = pd.read_csv(ruta + "races.csv")
    
    # Filtrar solo resultados con puntos válidos (no nulos)
    results_con_puntos = results[results['points'].notna()].copy()
    
    # Sumar todos los puntos por piloto a lo largo de su carrera
    print("🔢 Calculando puntos totales por piloto...")
    puntos_totales = results_con_puntos.groupby('driverId')['points'].sum().reset_index()
    
    # Unir con información de los pilotos
    tabla_historica = puntos_totales.merge(drivers, on='driverId', how='left')
    
    # Agregar información adicional
    # Contar carreras disputadas por piloto
    carreras_por_piloto = results.groupby('driverId').size().reset_index(name='carreras_disputadas')
    tabla_historica = tabla_historica.merge(carreras_por_piloto, on='driverId', how='left')
    
    # Contar victorias (posición = 1)
    victorias = results[results['position'] == '1'].groupby('driverId').size().reset_index(name='victorias')
    tabla_historica = tabla_historica.merge(victorias, on='driverId', how='left')
    tabla_historica['victorias'] = tabla_historica['victorias'].fillna(0)
    
    # Calcular promedio de puntos por carrera
    tabla_historica['puntos_promedio_carrera'] = tabla_historica['points'] / tabla_historica['carreras_disputadas']
    
    # Crear nombre completo del piloto
    tabla_historica['nombre_completo'] = tabla_historica['forename'] + ' ' + tabla_historica['surname']
    
    # Seleccionar y ordenar columnas finales
    columnas_finales = [
        'nombre_completo', 'nationality', 'points', 'carreras_disputadas', 
        'victorias', 'puntos_promedio_carrera', 'driverRef'
    ]
    
    tabla_final = tabla_historica[columnas_finales].copy()
    tabla_final.columns = [
        'Piloto', 'Nacionalidad', 'Puntos Totales', 'Carreras', 
        'Victorias', 'Puntos/Carrera', 'Código'
    ]
    
    # Ordenar por puntos totales (descendente)
    tabla_final = tabla_final.sort_values('Puntos Totales', ascending=False)
    tabla_final = tabla_final.reset_index(drop=True)
    
    # Redondear puntos promedio
    tabla_final['Puntos/Carrera'] = tabla_final['Puntos/Carrera'].round(2)
    
    return tabla_final, races['year'].min(), races['year'].max(), results, races, drivers

# Ejecutar la función
if __name__ == "__main__":
    tabla, año_inicio, año_fin, results, races, drivers = crear_tabla_historica_pilotos()
    
    print(f"\n🏆 TABLA HISTÓRICA DE PILOTOS F1 ({año_inicio}-{año_fin})")
    print("=" * 80)
    
    # Mostrar el TOP 20
    print("\n🥇 TOP 20 PILOTOS CON MÁS PUNTOS EN LA HISTORIA:")
    print(tabla.head(20).to_string(index=False))
    
    print(f"\n📈 ESTADÍSTICAS GENERALES:")
    print(f"• Total de pilotos en la historia: {len(tabla):,}")
    print(f"• Puntos máximos obtenidos: {tabla['Puntos Totales'].max():,.0f} ({tabla.iloc[0]['Piloto']})")
    print(f"• Promedio de carreras por piloto: {tabla['Carreras'].mean():.1f}")
    print(f"• Piloto con más victorias: {tabla.loc[tabla['Victorias'].idxmax(), 'Piloto']} ({tabla['Victorias'].max():.0f} victorias)")
    
    # Guardar en CSV si se desea
    # tabla.to_csv("tabla_historica_pilotos_f1.csv", index=False, encoding='utf-8')
    # print("\n💾 Tabla guardada como 'tabla_historica_pilotos_f1.csv'")
    
    # Análisis histórico detallado de pilotos específicos
    analizar_pilotos_especificos(tabla, results, races, drivers)
