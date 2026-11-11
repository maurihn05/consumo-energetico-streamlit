# Casos de prueba: Calculadora de Consumo Energético de Laboratorio

## Fórmulas
- Consumo mensual (kWh) = Potencia (W) × Cantidad × Horas diarias × Días mensuales / 1000
- Costo mensual (S/) = Consumo mensual (kWh) × Tarifa (S/ por kWh)

Para los tres casos se utiliza una tarifa común de **S/ 0.70 por kWh**.

## Caso 1: Una computadora
**Datos de entrada**
- Nombre: Computadora
- Potencia: 200 W
- Cantidad: 2
- Horas diarias: 8
- Días mensuales: 22
- Tarifa: S/ 0.70 por kWh

**Resultados esperados**
- Consumo: 200 × 2 × 8 × 22 / 1000 = **70.40 kWh**
- Costo: 70.40 × 0.70 = **S/ 49.28**

## Caso 2: Un equipo de laboratorio
**Datos de entrada**
- Nombre: Microscopio
- Potencia: 50 W
- Cantidad: 4
- Horas diarias: 5
- Días mensuales: 20
- Tarifa: S/ 0.70 por kWh

**Resultados esperados**
- Consumo: 50 × 4 × 5 × 20 / 1000 = **20.00 kWh**
- Costo: 20.00 × 0.70 = **S/ 14.00**

## Caso 3: Comparación de dos equipos
**Datos de entrada**
- Equipo A: Aire acondicionado, 1500 W, cantidad 1, 6 horas diarias, 25 días al mes.
- Equipo B: Impresora, 500 W, cantidad 2, 2 horas diarias, 20 días al mes.
- Tarifa: S/ 0.70 por kWh

**Resultados esperados**
- Aire acondicionado: 1500 × 1 × 6 × 25 / 1000 = **225.00 kWh**; costo = **S/ 157.50**.
- Impresora: 500 × 2 × 2 × 20 / 1000 = **40.00 kWh**; costo = **S/ 28.00**.
- Consumo total: **265.00 kWh**.
- Costo total: **S/ 185.50**.
- Equipo con mayor consumo: **Aire acondicionado (225.00 kWh)**.

## Pruebas adicionales de validación
- Intentar agregar un equipo sin nombre: la aplicación debe mostrar un mensaje de error.
- Intentar ingresar potencia igual a cero: la aplicación debe rechazar el registro.
- Ingresar 25 horas diarias o 32 días mensuales: los controles deben impedir esos valores.
- Eliminar un equipo: debe desaparecer de la lista y los totales deben actualizarse.
- Descargar el CSV: el archivo debe contener los equipos y resultados calculados.
