### List of origin-destination pairs for convergence check ###
# 142   = Erottaja
# 2370  = Matinkyla
# 2633  = Kauklahti
# 4120  = Martinlaakso
# 4492  = Tikkurila
# 8315  = Klaukkala
# 11043 = Jarvenpaa
# 19042 = Lohja

# Origin-destination pairs, also time period specified (aht/pt/iht):
# [tp, origin zone number, destination zone number]
od_pairs_convergence = [["aht", 2633, 142],
                        ["aht", 2370, 142],
                        ["aht", 4120, 142],
                        ["aht", 4492, 142],
                        ["aht", 8315, 142],
                        ["aht", 11043, 142],
                        ["aht", 19042, 142], 
                        ["aht", 2370, 4492],
                        ["aht", 4492, 2370],
                        ["iht", 142, 2633],
                        ["iht", 142, 2370],
                        ["iht", 142, 4120],
                        ["iht", 142, 4492],
                        ["iht", 142, 8315],
                        ["iht", 142, 11043],
                        ["iht", 142, 19042], 
                        ["iht", 2370, 4492],
                        ["iht", 4492, 2370]]