## Laberinto de Tom y Jerry

#muro (no se puede cruzar)=#
#salida = s
# Tom(gato) = T
# jerry(raton) = J
import copy
laberinto_original = [
    list("###############"),
    list("#J     #     T#"),
    list("##            #"),
    list("# #    #      #"),
    list("#      ##     #"),
    list("#       #     #"),
    list("#       ###   #"),
    list("#         #   #"),
    list("#  #     #    #"),
    list("#             #"),
    list("# #           #"),
    list("#   #         #"),
    list("#        #    #"),
    list("# S    #   #  #"),
    list("###############")#lista de listas
    ]
laberinto = copy.deepcopy(laberinto_original)

movimientos_tom = {
    "w": (-1, 0),  # subir: fila -1
    "s": (1, 0),   # bajar: fila +1
    "a": (0, -1),  # izquierda: columna -1
    "d": (0, 1),    # derecha: columna +1

}
movimientos_jerry= {
    "8": (-1, 0), # subir : fila -1
    "5": (1, 0),   # bajar: fila +1
    "4": (0, -1),  # izquierda: columna -1
    "6": (0, 1)    # derecha: columna +1

}

def mostrar_laberinto():
    simbolos = {
        "#": "🧱",
        "T": "🐱",
        "J": "🐭",
        "S": "🚪",
        " ": "⬛"
    }
    for fila in laberinto:
      print("".join(simbolos.get(celda, celda)for celda in fila))
print("Bienvenidos al juego de Tom y Jerry")






def prota_posicion(laberinto): #funcion para encontrar la posicion incial de los pj
  posi_tom = None #para poder reubicar ambos personajes
  posi_jerry = None

  for i, fila in enumerate(laberinto): #para poder identificar en que fila estan
    for j, colummna in enumerate(fila): #para poder identificar en que columna estan
      if colummna == "T": 
        posi_tom = (i, j)#ubica la posicion de T
      elif colummna == "J": 
        posi_jerry = (i, j)#ubica la posicion de j, i
  return posi_tom, posi_jerry #devuelve ambas posicionesd


#funcion distancia manhatan
def dista_manhatan (pos1, pos2):
  return abs(pos1[0]- pos2[0])+ abs(pos1[1]- pos2[1])

#funcion evaluacion de estado
def evaluar(estado):
  posi_tom, posi_jerry = prota_posicion(estado) #analizar esta parte
  posi_salida = None

  for f in range(len(estado)):
    for c in range(len(estado[0])):
      if estado[f][c] == "S":
        posi_salida = (f , c)

  if not posi_salida:
    return 9999
  #calculo de puntuacion
  if posi_jerry == posi_salida:
    return 10000 #jerry gana
  if posi_jerry == posi_tom:
    return -10000 # atraparon a jerry
  #calculo de distancia
  dist_jerry_salida = dista_manhatan(posi_jerry, posi_salida)
  dist_tom_jerry = dista_manhatan(posi_tom, posi_jerry)
  puntaje =  dist_tom_jerry - dist_jerry_salida
  return puntaje

# funcion de movimiento en base a minimax
def mover_personaje(estado, personaje, direccion, mapa_mov):
  nuevo_estado= copy.deepcopy(estado)  # Copia el laberinto para no modificar el original
  pos_actual = None
  for f in range(len( nuevo_estado)): # Buscar posición actual
    for c in range(len( nuevo_estado[0])):
      if nuevo_estado[f][c] == personaje:
        pos_actual = (f , c)
        break
    if pos_actual: #rompemos el bucle externo si se conoce la posicion
      break
  if pos_actual is None:
    return estado #no se encuentra el personaje , no hacer nada
  
  df, dc = mapa_mov[direccion]
  nf, nc = pos_actual[0] + df, pos_actual[1] + dc
  
  if 0 <= nf < len(nuevo_estado) and 0 <= nc < len(nuevo_estado[0]):
    if nuevo_estado [nf][nc] != "#":
      nuevo_estado[pos_actual[0]][pos_actual[1]] = " " #limpia la posi antenrior
      nuevo_estado [nf][nc] = personaje #mueve al personaje
  return nuevo_estado # Si no se pudo mover, devuelve el estado sin cambios

def ob_movimeintos_validos( estado, personaje, mapa_mov):
  movimientos_validos = []
  pos_actual = None
  for f in range(len(estado)):
    for c in range(len(estado[0])):
      if estado [f][c] == personaje :
        pos_actual = (f, c)
        break
    if pos_actual:
      break
  if pos_actual is None:
    return[] #no hay movimientos posibles
  for direccion, (df, dc) in mapa_mov.items():
    nf,nc = pos_actual[0] + df, pos_actual[1] + dc
    if 0 <= nf < len(estado) and 0 <= nc < len(estado[0]):
      if estado [nf][nc]!= "#":
        movimientos_validos.append(direccion)
  return movimientos_validos



#funcion minimax
def minimax(estado, profundidad, es_maximizador):
  if profundidad == 0:
    return evaluar(estado) , None
  
  if es_maximizador:
    mejor_valor = float("-inf")
    mejor_mov = None
    for mov in ob_movimeintos_validos(estado, "J", movimientos_jerry):
      #print("Movimientos válidos de Jerry:", ob_movimeintos_validos(estado, "J", movimientos_jerry))
      nuevo_estado = mover_personaje(estado, "J", mov, movimientos_jerry)
    
      valor, _ = minimax(nuevo_estado, profundidad - 1, False)
      if valor > mejor_valor:
        mejor_valor = valor
        mejor_mov = mov
    return mejor_valor, mejor_mov
  
  else:
    mejor_valor = float("inf")
    mejor_mov = None
    for mov in ob_movimeintos_validos(estado , "T", movimientos_tom):
      #print("Movimientos válidos de Tom:", ob_movimeintos_validos(estado, "T", movimientos_tom))
      nuevo_estado = mover_personaje(estado, "T", mov, movimientos_tom)
      valor, _ = minimax(nuevo_estado, profundidad - 1, True)
      if valor < mejor_valor:
        mejor_valor = valor
        mejor_mov = mov
      # mejor_valor = min(mejor_valor, valor)
    return mejor_valor, mejor_mov




prof_minimax = 5
while True:
  _ , mov_jerry = minimax(laberinto, prof_minimax, True)
  #print("Movimiento elegido por Jerry:", mov_jerry)
  if mov_jerry:
    laberinto = mover_personaje(laberinto, "J", mov_jerry, movimientos_jerry)
  posi_tom, posi_jerry = prota_posicion(laberinto)
  if posi_jerry == posi_tom:
    print("hoy se cena exclamo tom")
    mostrar_laberinto()
    break
  if laberinto[posi_jerry[0]][posi_jerry[1]] == "S":
    print("🧀 Jerry llegó a la salida y le dio con un mazo a Tom 🔨")
    mostrar_laberinto()
    break
  mostrar_laberinto()

  _, mov_tom = minimax(laberinto, prof_minimax , False)
  #print("Movimiento elegido por Tom:", mov_tom)
  if mov_tom:
    laberinto = mover_personaje(laberinto, "T", mov_tom, movimientos_tom)
  posi_tom, posi_jerry = prota_posicion(laberinto)

  if posi_tom == posi_jerry:
    print("'Hoy se cena' exclamó Tom")
    mostrar_laberinto()
    break
