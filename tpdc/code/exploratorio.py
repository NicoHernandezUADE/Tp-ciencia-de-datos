import pandas as pd
import numpy as np
import os
from datetime import datetime

def analizar_tendencias_escuderias_ultimos_20_años():
    """
    Análisis completo de tendencias históricas, correlaciones y evolución de escuderías
    en los últimos 20 años (2004-2024)
    """
    # Obtener la ruta a los archivos
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(script_dir, "..", "archive") + os.sep
    
    print("="*100)
    print("🏎️ ANÁLISIS DE TENDENCIAS HISTÓRICAS DE ESCUDERÍAS F1 (2004-2024)")
    print("="*100)
    
    # Verificar que el directorio existe
    if not os.path.exists(ruta):
        print(f"❌ Error: No se encontró el directorio {ruta}")
        return None
    
    try:
        # Cargar datos necesarios
        print("📂 Cargando datos...")
        constructors = pd.read_csv(ruta + "constructors.csv")
        constructor_standings = pd.read_csv(ruta + "constructor_standings.csv")
        constructor_results = pd.read_csv(ruta + "constructor_results.csv")
        races = pd.read_csv(ruta + "races.csv")
        results = pd.read_csv(ruta + "results.csv")
        
        print(f"✅ Datos cargados: {len(constructors)} constructores, {len(races)} carreras")
        
        # Filtrar últimos 20 años (2004-2024)
        año_inicio = 2004
        año_fin = 2024
        races_periodo = races[(races['year'] >= año_inicio) & (races['year'] <= año_fin)]
        
        print(f"🗓️ Período de análisis: {año_inicio}-{año_fin} ({len(races_periodo)} carreras)")
        
        # Análisis 1: Evolución de puntos por escudería por año
        print(f"\n{'='*80}")
        print("📈 EVOLUCIÓN DE PUNTOS POR ESCUDERÍA (2004-2024)")
        print(f"{'='*80}")
        
        # Unir datos para obtener puntos por constructor por año
        constructor_standings_periodo = constructor_standings.merge(
            races_periodo[['raceId', 'year']], on='raceId'
        )
        
        # Agrupar por año y constructor para obtener puntos máximos (final de temporada)
        puntos_por_año = constructor_standings_periodo.groupby(['year', 'constructorId']).agg({
            'points': 'max',
            'position': 'min',
            'wins': 'max'
        }).reset_index()
        
        # Agregar nombres de constructores
        puntos_por_año = puntos_por_año.merge(
            constructors[['constructorId', 'name', 'nationality']], 
            on='constructorId'
        )
        
        # Top 5 escuderías por puntos totales en el período
        puntos_totales = puntos_por_año.groupby(['constructorId', 'name']).agg({
            'points': 'sum',
            'wins': 'sum',
            'position': 'mean'
        }).sort_values('points', ascending=False)
        
        print("🏆 TOP 10 ESCUDERÍAS POR PUNTOS TOTALES (2004-2024):")
        for i, (_, row) in enumerate(puntos_totales.head(10).iterrows(), 1):
            print(f"{i:2d}. {row.name[1]:<20}: {row['points']:6.0f} puntos, "
                  f"{row['wins']:3.0f} victorias, pos. promedio: {row['position']:.1f}")
        
        # Análisis 2: Correlaciones entre variables
        print(f"\n{'='*80}")
        print("🔗 ANÁLISIS DE CORRELACIONES")
        print(f"{'='*80}")
        
        # Preparar datos para correlaciones
        datos_correlacion = puntos_por_año.groupby('constructorId').agg({
            'points': ['mean', 'std', 'sum'],
            'wins': ['sum', 'mean'],
            'position': ['mean', 'std']
        }).reset_index()
        
        # Aplanar nombres de columnas
        datos_correlacion.columns = [
            'constructorId', 'puntos_promedio', 'puntos_variabilidad', 'puntos_total',
            'victorias_total', 'victorias_promedio', 'posicion_promedio', 'posicion_variabilidad'
        ]
        
        # Calcular correlaciones
        correlaciones = datos_correlacion.select_dtypes(include=[np.number]).corr()
        
        print("📊 CORRELACIONES PRINCIPALES:")
        print(f"• Puntos totales vs Victorias totales: {correlaciones.loc['puntos_total', 'victorias_total']:.3f}")
        print(f"• Puntos promedio vs Posición promedio: {correlaciones.loc['puntos_promedio', 'posicion_promedio']:.3f}")
        print(f"• Victorias vs Posición promedio: {correlaciones.loc['victorias_total', 'posicion_promedio']:.3f}")
        print(f"• Variabilidad puntos vs Variabilidad posición: {correlaciones.loc['puntos_variabilidad', 'posicion_variabilidad']:.3f}")
        
        # Análisis 3: Tendencias temporales por escudería líder
        print(f"\n{'='*80}")
        print("📊 EVOLUCIÓN TEMPORAL DE ESCUDERÍAS LÍDERES")
        print(f"{'='*80}")
        
        # Escuderías más exitosas para análisis detallado
        top_constructores = puntos_totales.head(6).index.tolist()
        
        print("🎯 ANÁLISIS DETALLADO DE TOP 6 ESCUDERÍAS:")
        
        for constructor_id, name in top_constructores:
            datos_constructor = puntos_por_año[puntos_por_año['constructorId'] == constructor_id].sort_values('year')
            
            if len(datos_constructor) > 0:
                print(f"\n🏎️ {name.upper()}:")
                print(f"   • Años activos en período: {len(datos_constructor)}")
                print(f"   • Mejor año: {datos_constructor.loc[datos_constructor['points'].idxmax(), 'year']} "
                      f"({datos_constructor['points'].max():.0f} puntos)")
                print(f"   • Peor año: {datos_constructor.loc[datos_constructor['points'].idxmin(), 'year']} "
                      f"({datos_constructor['points'].min():.0f} puntos)")
                print(f"   • Tendencia puntos: ", end="")
                
                # Calcular tendencia simple (primeros 5 años vs últimos 5 años)
                if len(datos_constructor) >= 10:
                    primeros_5 = datos_constructor.head(5)['points'].mean()
                    ultimos_5 = datos_constructor.tail(5)['points'].mean()
                    if ultimos_5 > primeros_5 * 1.1:
                        print("📈 Mejorando")
                    elif ultimos_5 < primeros_5 * 0.9:
                        print("📉 Declinando")
                    else:
                        print("➡️ Estable")
                else:
                    print("➡️ Datos insuficientes")
                
                # Mostrar evolución año a año (últimos 10 años)
                ultimos_años = datos_constructor.tail(10)
                print("   • Últimos años: ", end="")
                for _, row in ultimos_años.iterrows():
                    print(f"{int(row['year'])}({row['points']:.0f}pts) ", end="")
                print()
        
        # Análisis 4: Dominancia y competitividad
        print(f"\n{'='*80}")
        print("👑 ANÁLISIS DE DOMINANCIA Y COMPETITIVIDAD")
        print(f"{'='*80}")
        
        # Calcular dominancia por año (diferencia entre 1° y 2°)
        dominancia_por_año = []
        
        for año in range(año_inicio, año_fin + 1):
            datos_año = puntos_por_año[puntos_por_año['year'] == año].sort_values('points', ascending=False)
            if len(datos_año) >= 2:
                primero = datos_año.iloc[0]
                segundo = datos_año.iloc[1]
                diferencia = primero['points'] - segundo['points']
                dominancia_por_año.append({
                    'year': año,
                    'constructor_1': primero['name'],
                    'puntos_1': primero['points'],
                    'constructor_2': segundo['name'],
                    'puntos_2': segundo['points'],
                    'diferencia': diferencia,
                    'porcentaje_dominancia': (diferencia / primero['points'] * 100) if primero['points'] > 0 else 0
                })
        
        dominancia_df = pd.DataFrame(dominancia_por_año)
        
        print("🥇 AÑOS CON MAYOR DOMINANCIA (top 5):")
        top_dominancia = dominancia_df.nlargest(5, 'diferencia')
        for _, row in top_dominancia.iterrows():
            print(f"   {int(row['year'])}: {row['constructor_1']} ({row['puntos_1']:.0f}pts) "
                  f"vs {row['constructor_2']} ({row['puntos_2']:.0f}pts) "
                  f"- Diferencia: {row['diferencia']:.0f}pts ({row['porcentaje_dominancia']:.1f}%)")
        
        print("\n🤝 AÑOS MÁS COMPETITIVOS (menor diferencia):")
        top_competitivos = dominancia_df.nsmallest(5, 'diferencia')
        for _, row in top_competitivos.iterrows():
            print(f"   {int(row['year'])}: {row['constructor_1']} ({row['puntos_1']:.0f}pts) "
                  f"vs {row['constructor_2']} ({row['puntos_2']:.0f}pts) "
                  f"- Diferencia: {row['diferencia']:.0f}pts ({row['porcentaje_dominancia']:.1f}%)")
        
        # Análisis 5: Ascensos y caídas más dramáticas
        print(f"\n{'='*80}")
        print("🎢 ASCENSOS Y CAÍDAS MÁS DRAMÁTICAS")
        print(f"{'='*80}")
        
        cambios_dramaticos = []
        
        for constructor_id, name in puntos_totales.head(15).index.tolist():
            datos_constructor = puntos_por_año[puntos_por_año['constructorId'] == constructor_id].sort_values('year')
            
            if len(datos_constructor) >= 3:
                # Buscar mayor ascenso y caída año a año
                datos_constructor['cambio_puntos'] = datos_constructor['points'].diff()
                
                mayor_ascenso = datos_constructor.loc[datos_constructor['cambio_puntos'].idxmax()]
                mayor_caida = datos_constructor.loc[datos_constructor['cambio_puntos'].idxmin()]
                
                if not pd.isna(mayor_ascenso['cambio_puntos']):
                    cambios_dramaticos.append({
                        'tipo': 'Ascenso',
                        'constructor': name,
                        'año': int(mayor_ascenso['year']),
                        'cambio': mayor_ascenso['cambio_puntos'],
                        'puntos_anteriores': mayor_ascenso['points'] - mayor_ascenso['cambio_puntos'],
                        'puntos_nuevos': mayor_ascenso['points']
                    })
                
                if not pd.isna(mayor_caida['cambio_puntos']):
                    cambios_dramaticos.append({
                        'tipo': 'Caída',
                        'constructor': name,
                        'año': int(mayor_caida['year']),
                        'cambio': mayor_caida['cambio_puntos'],
                        'puntos_anteriores': mayor_caida['points'] - mayor_caida['cambio_puntos'],
                        'puntos_nuevos': mayor_caida['points']
                    })
        
        cambios_df = pd.DataFrame(cambios_dramaticos)
        
        if len(cambios_df) > 0:
            print("📈 MAYORES ASCENSOS:")
            ascensos = cambios_df[cambios_df['tipo'] == 'Ascenso'].nlargest(5, 'cambio')
            for _, row in ascensos.iterrows():
                print(f"   {row['constructor']} ({row['año']}): {row['puntos_anteriores']:.0f} → "
                      f"{row['puntos_nuevos']:.0f} pts (+{row['cambio']:.0f})")
            
            print("\n📉 MAYORES CAÍDAS:")
            caidas = cambios_df[cambios_df['tipo'] == 'Caída'].nsmallest(5, 'cambio')
            for _, row in caidas.iterrows():
                print(f"   {row['constructor']} ({row['año']}): {row['puntos_anteriores']:.0f} → "
                      f"{row['puntos_nuevos']:.0f} pts ({row['cambio']:.0f})")
        
        # Análisis 6: Resumen estadístico final
        print(f"\n{'='*80}")
        print("📊 RESUMEN ESTADÍSTICO PERÍODO 2004-2024")
        print(f"{'='*80}")
        
        total_constructores = len(puntos_por_año['constructorId'].unique())
        total_temporadas = len(puntos_por_año['year'].unique())
        
        print(f"📈 ESTADÍSTICAS GENERALES:")
        print(f"   • Total de constructores activos: {total_constructores}")
        print(f"   • Temporadas analizadas: {total_temporadas}")
        print(f"   • Puntos promedio por temporada: {puntos_por_año['points'].mean():.1f}")
        print(f"   • Constructor más exitoso: {puntos_totales.index[0][1]} ({puntos_totales.iloc[0]['points']:.0f} puntos)")
        print(f"   • Período más competitivo: {dominancia_df.loc[dominancia_df['diferencia'].idxmin(), 'year']:.0f}")
        print(f"   • Período menos competitivo: {dominancia_df.loc[dominancia_df['diferencia'].idxmax(), 'year']:.0f}")
        
        return {
            'puntos_por_año': puntos_por_año,
            'correlaciones': correlaciones,
            'dominancia': dominancia_df,
            'cambios_dramaticos': cambios_df,
            'puntos_totales': puntos_totales
        }
        
    except Exception as e:
        print(f"❌ Error durante el análisis: {str(e)}")
        return None

if __name__ == "__main__":
    print("🚀 Iniciando análisis de tendencias históricas de escuderías F1...")
    resultados = analizar_tendencias_escuderias_ultimos_20_años()
    
    if resultados:
        print(f"\n✅ Análisis completado exitosamente!")
        print("📊 Los datos están disponibles en las variables de retorno para análisis adicionales.")
    else:
        print("\n❌ El análisis no pudo completarse.")
