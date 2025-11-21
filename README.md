# Análisis de Datos Formula 1 - Proyecto de Ciencia de Datos


## 📦 Dependencias e Instalación

### Entorno Virtual
```bash
# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual (Windows)
.venv\Scripts\activate

# Activar entorno virtual (Mac/Linux)
source .venv/bin/activate
```

### Dependencias Principales Instaladas

#### 📊 Análisis de Datos Base
```bash
pip install pandas numpy
```
- **pandas**: Manipulación y análisis de datos CSV
- **numpy**: Cálculos numéricos y operaciones matemáticas

#### 🏎️ Análisis Avanzado F1
```bash
pip install fastf1
```
- **FastF1**: Acceso a telemetría oficial de F1 (2018-presente)
  - Datos de tiempo de vuelta en tiempo real
  - Condiciones meteorológicas por carrera
  - Datos GPS de trazado
  - Telemetría de velocidad y throttle

#### 📈 Visualización y Gráficos
```bash
pip install matplotlib seaborn
```
- **matplotlib**: Librería base para gráficos
- **seaborn**: Gráficos estadísticos avanzados

### Instalación Completa
```bash
pip install pandas numpy fastf1 matplotlib seaborn
```