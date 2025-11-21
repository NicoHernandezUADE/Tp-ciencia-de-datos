import pandas as pd
import os

def analizar_archivos_con_describe():
    """
    Aplica la función .describe() de pandas a todos los archivos CSV
    para obtener estadísticas descriptivas completas
    """
    # Obtener la ruta a los archivos
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(script_dir, "..", "archive") + os.sep
    
    print("="*90)
    print("📊 ANÁLISIS ESTADÍSTICO DESCRIPTIVO DE ARCHIVOS F1 CON .describe()")
    print("="*90)
    
    # Lista de archivos CSV a analizar
    archivos = [
        "circuits.csv",
        "constructor_results.csv",
        "constructor_standings.csv",
        "constructors.csv",
        "driver_standings.csv",
        "drivers.csv",
        "lap_times.csv",
        "pit_stops.csv",
        "qualifying.csv",
        "races.csv",
        "results.csv",
        "seasons.csv",
        "sprint_results.csv",
        "status.csv"
    ]
    
    # Verificar que el directorio existe
    if not os.path.exists(ruta):
        print(f"❌ Error: No se encontró el directorio {ruta}")
        return
    
    print(f"🔍 Analizando archivos en: {ruta}")
    print()
    
    for archivo in archivos:
        try:
            print(f"\n{'='*80}")
            print(f"📁 ARCHIVO: {archivo.upper()}")
            print(f"{'='*80}")
            
            # Cargar el archivo
            df = pd.read_csv(ruta + archivo)
            
            print(f"📊 INFORMACIÓN GENERAL:")
            print(f"   • Forma del dataset: {df.shape[0]:,} filas × {df.shape[1]} columnas")
            print(f"   • Memoria utilizada: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
            
            # Información de tipos de datos
            print(f"\n🔢 TIPOS DE DATOS:")
            tipos = df.dtypes.value_counts()
            for tipo, cantidad in tipos.items():
                print(f"   • {tipo}: {cantidad} columnas")
            
            # Valores nulos
            nulos = df.isnull().sum()
            total_nulos = nulos.sum()
            print(f"\n❓ VALORES NULOS:")
            print(f"   • Total de valores nulos: {total_nulos:,}")
            if total_nulos > 0:
                print(f"   • Porcentaje de valores nulos: {(total_nulos / (df.shape[0] * df.shape[1]) * 100):.2f}%")
                print("   • Columnas con valores nulos:")
                for col, nul in nulos[nulos > 0].items():
                    print(f"     - {col}: {nul:,} ({nul/len(df)*100:.1f}%)")
            else:
                print("   • ✅ No hay valores nulos")
            
            # Análisis describe para columnas numéricas
            columnas_numericas = df.select_dtypes(include=['number']).columns
            if len(columnas_numericas) > 0:
                print(f"\n📈 ESTADÍSTICAS DESCRIPTIVAS (COLUMNAS NUMÉRICAS):")
                print(f"   • Columnas numéricas encontradas: {len(columnas_numericas)}")
                print(f"   • Columnas: {', '.join(columnas_numericas)}")
                print()
                
                desc_num = df[columnas_numericas].describe()
                print(desc_num.to_string())
                
                # Análisis adicional para columnas numéricas
                print(f"\n🔍 ANÁLISIS ADICIONAL COLUMNAS NUMÉRICAS:")
                for col in columnas_numericas:
                    valores_unicos = df[col].nunique()
                    print(f"   • {col}: {valores_unicos:,} valores únicos")
                    if valores_unicos <= 20:  # Si hay pocos valores únicos, mostrar la distribución
                        print(f"     Distribución: {dict(df[col].value_counts().head())}")
            else:
                print(f"\n📈 ESTADÍSTICAS DESCRIPTIVAS:")
                print("   • No se encontraron columnas numéricas")
            
            # Análisis describe para columnas categóricas/objeto
            columnas_objeto = df.select_dtypes(include=['object']).columns
            if len(columnas_objeto) > 0:
                print(f"\n📝 ESTADÍSTICAS DESCRIPTIVAS (COLUMNAS DE TEXTO):")
                print(f"   • Columnas de texto encontradas: {len(columnas_objeto)}")
                print(f"   • Columnas: {', '.join(columnas_objeto)}")
                print()
                
                desc_obj = df[columnas_objeto].describe()
                print(desc_obj.to_string())
                
                # Análisis adicional para columnas de texto
                print(f"\n🔍 ANÁLISIS ADICIONAL COLUMNAS DE TEXTO:")
                for col in columnas_objeto:
                    valores_unicos = df[col].nunique()
                    print(f"   • {col}: {valores_unicos:,} valores únicos")
                    if valores_unicos <= 10:  # Si hay pocos valores únicos, mostrar todos
                        print(f"     Valores: {list(df[col].unique())}")
                    elif valores_unicos <= 20:  # Si hay algunos valores, mostrar los más frecuentes
                        print(f"     Top valores: {list(df[col].value_counts().head().index)}")
            
            # Duplicados
            duplicados = df.duplicated().sum()
            print(f"\n🔄 REGISTROS DUPLICADOS:")
            print(f"   • Total de filas duplicadas: {duplicados:,}")
            if duplicados > 0:
                print(f"   • Porcentaje de duplicados: {(duplicados/len(df)*100):.2f}%")
            else:
                print("   • ✅ No hay registros duplicados")
            
            print(f"\n✅ Análisis de {archivo} completado")
            
        except Exception as e:
            print(f"❌ Error al procesar {archivo}: {str(e)}")
            continue
    
    print(f"\n{'='*90}")
    print("🎯 RESUMEN FINAL")
    print(f"{'='*90}")
    print("✅ Análisis descriptivo completado para todos los archivos")
    print("📊 Se aplicó .describe() a columnas numéricas y de texto")
    print("🔍 Se analizaron tipos de datos, valores nulos y duplicados")
    print("📈 Se proporcionaron estadísticas adicionales relevantes")

if __name__ == "__main__":
    analizar_archivos_con_describe()