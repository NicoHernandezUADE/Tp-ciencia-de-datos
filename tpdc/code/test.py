import pandas as pd
import os
from datetime import datetime

def analizar_carreras_2024():
    """
    Análisis de las carreras del año 2024 que incluye:
    - Edad del piloto
    - País del piloto 
    - Diferencia de tiempos entre piloto 1 y 2
    """
    
    # Obtener la ruta a los archivos
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(script_dir, "..", "archive") + os.sep
    
    print("="*90)
    print("🏎️ ANÁLISIS DE CARRERAS F1 - TEMPORADA 2024")
    print("="*90)
    
    try:
        # Cargar los datos necesarios
        print("📂 Cargando datos...")
        drivers = pd.read_csv(ruta + "drivers.csv")
        results = pd.read_csv(ruta + "results.csv")
        races = pd.read_csv(ruta + "races.csv")
        
        print(f"✅ Datos cargados exitosamente!")
        print(f"   • Pilotos: {len(drivers)} registros")
        print(f"   • Resultados: {len(results)} registros")
        print(f"   • Carreras: {len(races)} registros")
        
    except FileNotFoundError as e:
        print(f"❌ Error al cargar archivos: {e}")
        return None
    
    # Filtrar carreras del 2024
    carreras_2024 = races[races['year'] == 2024].copy()
    print(f"\n🗓️ Carreras en 2024: {len(carreras_2024)}")
    
    if len(carreras_2024) == 0:
        print("❌ No se encontraron carreras del 2024")
        return None
    
    # Obtener resultados de 2024
    race_ids_2024 = carreras_2024['raceId'].tolist()
    resultados_2024 = results[results['raceId'].isin(race_ids_2024)].copy()
    
    # Unir datos
    datos_completos = resultados_2024.merge(carreras_2024[['raceId', 'name', 'date']], on='raceId')
    datos_completos = datos_completos.merge(drivers[['driverId', 'driverRef', 'forename', 'surname', 'dob', 'nationality']], on='driverId')
    
    # Calcular edad de los pilotos al momento de cada carrera
    def calcular_edad(fecha_nacimiento, fecha_carrera):
        try:
            nac = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')
            carr = datetime.strptime(fecha_carrera, '%Y-%m-%d')
            edad = carr.year - nac.year - ((carr.month, carr.day) < (nac.month, nac.day))
            return edad
        except:
            return None
    
    datos_completos['edad_en_carrera'] = datos_completos.apply(
        lambda row: calcular_edad(row['dob'], row['date']), axis=1
    )
    
    # Crear nombre completo del piloto
    datos_completos['nombre_completo'] = datos_completos['forename'] + ' ' + datos_completos['surname']
    
    print(f"📊 Resultados procesados: {len(datos_completos)}")
    
    # ===== ANÁLISIS POR EDAD =====
    print(f"\n👶 ANÁLISIS POR EDAD DE PILOTOS EN 2024:")
    print("-" * 60)
    
    # Estadísticas de edad
    edad_stats = datos_completos.groupby('nombre_completo').agg({
        'edad_en_carrera': 'first',
        'nationality': 'first',
        'raceId': 'count',
        'points': 'sum'
    }).reset_index()
    edad_stats.columns = ['Piloto', 'Edad', 'Nacionalidad', 'Carreras', 'Puntos_Total']
    edad_stats = edad_stats.sort_values('Edad')
    
    print("🔢 Estadísticas generales de edad:")
    print(f"   • Piloto más joven: {edad_stats.iloc[0]['Piloto']} ({edad_stats.iloc[0]['Edad']} años)")
    print(f"   • Piloto más veterano: {edad_stats.iloc[-1]['Piloto']} ({edad_stats.iloc[-1]['Edad']} años)")
    print(f"   • Edad promedio: {edad_stats['Edad'].mean():.1f} años")
    print(f"   • Rango de edades: {edad_stats['Edad'].min()} - {edad_stats['Edad'].max()} años")
    
    # Top pilotos jóvenes y veteranos
    print(f"\n👶 TOP 5 PILOTOS MÁS JÓVENES:")
    for i, (_, piloto) in enumerate(edad_stats.head(5).iterrows(), 1):
        print(f"   {i}. {piloto['Piloto']:<25} - {piloto['Edad']} años ({piloto['Nacionalidad']})")
    
    print(f"\n🧓 TOP 5 PILOTOS MÁS VETERANOS:")
    for i, (_, piloto) in enumerate(edad_stats.tail(5).iterrows(), 1):
        print(f"   {i}. {piloto['Piloto']:<25} - {piloto['Edad']} años ({piloto['Nacionalidad']})")
    
    # ===== ANÁLISIS POR PAÍS =====
    print(f"\n🌍 ANÁLISIS POR NACIONALIDAD EN 2024:")
    print("-" * 60)
    
    por_pais = edad_stats.groupby('Nacionalidad').agg({
        'Carreras': 'sum',
        'Puntos_Total': 'sum',
        'Piloto': 'count',
        'Edad': 'mean'
    }).reset_index()
    por_pais.columns = ['País', 'Total_Carreras', 'Puntos_Total', 'Num_Pilotos', 'Edad_Promedio']
    por_pais = por_pais.sort_values('Puntos_Total', ascending=False)
    
    print("🏆 TOP 10 PAÍSES POR PUNTOS TOTALES:")
    for i, (_, pais) in enumerate(por_pais.head(10).iterrows(), 1):
        print(f"   {i:2d}. {pais['País']:<15} - {pais['Puntos_Total']:6.1f} puntos, "
            f"{pais['Num_Pilotos']} piloto(s), edad prom: {pais['Edad_Promedio']:.1f} años")
    
    # ===== ANÁLISIS DE DIFERENCIAS DE TIEMPO =====
    print(f"\n⏱️ ANÁLISIS DE DIFERENCIAS DE TIEMPO 2024:")
    print("-" * 60)
    
    # Analizar diferencias de tiempo por carrera (posición 1 vs posición 2)
    diferencias_tiempo = []
    
    for race_id in carreras_2024['raceId']:
        resultados_carrera = datos_completos[datos_completos['raceId'] == race_id].copy()
        
        # Obtener información de la carrera
        info_carrera = carreras_2024[carreras_2024['raceId'] == race_id].iloc[0]
        
        # Filtrar solo posiciones válidas y ordenar
        resultados_validos = resultados_carrera[
            (resultados_carrera['position'] != '\\N') & 
            (resultados_carrera['position'].notna())
        ].copy()
        
        if len(resultados_validos) >= 2:
            # Convertir posición a int y ordenar
            resultados_validos['pos_int'] = resultados_validos['position'].astype(int)
            resultados_validos = resultados_validos.sort_values('pos_int')
            
            # Obtener primero y segundo lugar
            primero = resultados_validos.iloc[0]
            segundo = resultados_validos.iloc[1]
            
            # Calcular diferencia de tiempo si está disponible
            tiempo_diff = None
            if 'milliseconds' in resultados_validos.columns:
                if (primero['milliseconds'] != '\\N' and segundo['milliseconds'] != '\\N' and 
                    pd.notna(primero['milliseconds']) and pd.notna(segundo['milliseconds'])):
                    try:
                        tiempo_primero = float(primero['milliseconds'])
                        tiempo_segundo = float(segundo['milliseconds'])
                        tiempo_diff = (tiempo_segundo - tiempo_primero) / 1000  # Convertir a segundos
                    except:
                        tiempo_diff = None
            
            diferencias_tiempo.append({
                'carrera': info_carrera['name'],
                'fecha': info_carrera['date'],
                'piloto_1': primero['nombre_completo'],
                'edad_1': primero['edad_en_carrera'],
                'pais_1': primero['nationality'],
                'piloto_2': segundo['nombre_completo'],
                'edad_2': segundo['edad_en_carrera'],
                'pais_2': segundo['nationality'],
                'diferencia_tiempo': tiempo_diff,
                'diferencia_edad': abs(primero['edad_en_carrera'] - segundo['edad_en_carrera']) if (primero['edad_en_carrera'] and segundo['edad_en_carrera']) else None
            })
    
    df_diferencias = pd.DataFrame(diferencias_tiempo)
    
    print(f"🏁 ANÁLISIS DE GANADORES Y SEGUNDOS LUGARES:")
    print(f"   • Total de carreras analizadas: {len(df_diferencias)}")
    
    if len(df_diferencias) > 0:
        # Diferencias de tiempo válidas
        diff_validas = df_diferencias[df_diferencias['diferencia_tiempo'].notna()]
        
        if len(diff_validas) > 0:
            print(f"   • Carreras con tiempos válidos: {len(diff_validas)}")
            print(f"   • Diferencia promedio 1º-2º: {diff_validas['diferencia_tiempo'].mean():.3f} segundos")
            print(f"   • Diferencia mínima: {diff_validas['diferencia_tiempo'].min():.3f} segundos")
            print(f"   • Diferencia máxima: {diff_validas['diferencia_tiempo'].max():.3f} segundos")
        
        # Diferencias de edad
        diff_edad_validas = df_diferencias[df_diferencias['diferencia_edad'].notna()]
        if len(diff_edad_validas) > 0:
            print(f"   • Diferencia de edad promedio 1º-2º: {diff_edad_validas['diferencia_edad'].mean():.1f} años")
        
        print(f"\n🏆 DETALLE DE CADA CARRERA 2024:")
        for i, (_, carrera) in enumerate(df_diferencias.iterrows(), 1):
            print(f"\n{i:2d}. {carrera['carrera']} ({carrera['fecha']})")
            print(f"    🥇 1º: {carrera['piloto_1']:<20} ({carrera['edad_1']} años, {carrera['pais_1']})")
            print(f"    🥈 2º: {carrera['piloto_2']:<20} ({carrera['edad_2']} años, {carrera['pais_2']})")
            if carrera['diferencia_tiempo']:
                print(f"    ⏱️ Diferencia: {carrera['diferencia_tiempo']:.3f} segundos")
            if carrera['diferencia_edad']:
                print(f"    👥 Diferencia edad: {carrera['diferencia_edad']} años")
    
    # ===== RESUMEN ESTADÍSTICO =====
    print(f"\n📈 RESUMEN ESTADÍSTICO 2024:")
    print("-" * 60)
    print(f"• Total pilotos activos: {len(edad_stats)}")
    print(f"• Total países representados: {len(por_pais)}")
    print(f"• Total carreras: {len(carreras_2024)}")
    print(f"• Rango de edades: {edad_stats['Edad'].min()}-{edad_stats['Edad'].max()} años")
    
    return {
        'edad_stats': edad_stats,
        'por_pais': por_pais,
        'diferencias_tiempo': df_diferencias,
        'datos_completos': datos_completos
    }

# Ejecutar el análisis
if __name__ == "__main__":
    resultado = analizar_carreras_2024()
    if resultado:
        print("\n✅ Análisis completado exitosamente!")
    else:
        print("\n❌ No se pudo completar el análisis.")
