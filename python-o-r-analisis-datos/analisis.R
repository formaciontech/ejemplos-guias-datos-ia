# La misma consulta en R con arrow y dplyr, leyendo el Parquet que genera Python.
# Guía: https://formaciontech.es/guias/python-o-r-analisis-datos/
#
# Ejecuta antes generar_datos.py y tres_motores.py. Después:
#   Rscript analisis.R
# Con renv, guarda las versiones con renv::snapshot() y recupéralas en otro
# equipo con renv::restore().

library(arrow)
library(dplyr)

ventas <- read_parquet("datos/ventas.parquet")

resumen <- ventas |>
  filter(as.Date(fecha) >= as.Date("2026-01-01"),
         as.Date(fecha) <  as.Date("2026-04-01")) |>
  group_by(tienda) |>
  summarise(unidades = sum(unidades), importe = sum(importe)) |>
  arrange(tienda)

print(resumen)

# Cifra de control: el resultado debe coincidir con el de Python
python <- read.csv("datos/resumen_python.csv")
stopifnot(all.equal(resumen$unidades, python$unidades),
          all.equal(resumen$importe, python$importe, tolerance = 1e-9))
cat("R y Python coinciden.\n")
