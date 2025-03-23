from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional

class Istasyon:
    def __init__(self, idx: str, ad: str, hat: str): # Defining metro stations
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = []  # (station, time) tuples

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int): # Adding neighbors to stations
        self.komsular.append((istasyon, sure))

class MetroAgi: # Defining metro network
    def __init__(self): # Initializing stations and lines
        self.istasyonlar: Dict[str, Istasyon] = {}
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None: # Adding stations to the network
        if id not in self.istasyonlar:
            istasyon = Istasyon(idx, ad, hat)
            self.istasyonlar[idx] = istasyon
            self.hatlar[hat].append(istasyon)

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None: # Adding connections between stations
        istasyon1 = self.istasyonlar[istasyon1_id]
        istasyon2 = self.istasyonlar[istasyon2_id]
        istasyon1.komsu_ekle(istasyon2, sure)
        istasyon2.komsu_ekle(istasyon1, sure)
    
    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[List[Istasyon]]: # Finding the route with minimum transfers using BFS
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar: # If the starting or ending station is not in the network, return None
            return None
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        ziyaret_edildi = {baslangic}
        kuyruk = deque([(baslangic, [baslangic])])
        while kuyruk: # While there are stations in the queue
            mevcut, yol = kuyruk.popleft() # Get the current station and route
            
            if mevcut == hedef: # If the current station is the destination, return the route
                return yol
            
            for komsu, _ in mevcut.komsular: # For each neighbor of the current station
                if komsu not in ziyaret_edildi: # If the neighbor is not visited
                    ziyaret_edildi.add(komsu) # Mark the neighbor as visited
                    kuyruk.append((komsu, yol + [komsu])) # Add the neighbor to the queue with the route
        
        return None

    def _heuristic(self, mevcut: Istasyon, hedef: Istasyon) -> int: # Simple heuristic based on station indices to estimate minimum travel time
        # Extract station indices (e.g., "K1" -> 1, "M2" -> 2)
        mevcut_index = int(mevcut.idx[1:])
        hedef_index = int(hedef.idx[1:])
    
        if mevcut.hat == hedef.hat:
            return 2 * abs(mevcut_index - hedef_index) # If on the same line, use index difference with a 2-minute base rate
        else:
            return 2 * abs(mevcut_index - hedef_index) + 2 # If on different lines, add a 2-minute transfer penalty to the base rate
            
    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int]]: # Finding the fastest route using A* algorithm
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar: # If the starting or ending station is not in the network, return None
            return None

        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]
        ziyaret_edildi = set()
        pq = []
        index = 0  # Unique index to prevent comparison issues in heap
        
        maliyet_g = {baslangic: 0} # Actual cost (time) from the start to each station
        maliyet_f = {baslangic: self._heuristic(baslangic, hedef)} # Estimated total cost from start to target via each station

        heapq.heappush(pq, (maliyet_f[baslangic], 0, index, baslangic, [baslangic])) # Add the starting station to the priority queue

        while pq:  # Continue while there are stations in the queue
            _, maliyet_g_mevcut, _, mevcut, yol = heapq.heappop(pq)  # Get the station with the lowest maliyet_f

            if mevcut == hedef:  # If the target is reached, return the path and total time
                return yol, maliyet_g_mevcut

            if mevcut in ziyaret_edildi:  # Skip if the station has already been processed
                continue
            
            ziyaret_edildi.add(mevcut)  # Mark the station as visited
            
            for komsu, sure in mevcut.komsular: # Check all neighbors of the current station
                yeni_maliyet_g = maliyet_g_mevcut + sure # Calculate the actual cost to reach the neighbor

                if komsu not in maliyet_g or yeni_maliyet_g < maliyet_g[komsu]: # Update if this path to the neighbor is shorter or the neighbor is unvisited
                    maliyet_g[komsu] = yeni_maliyet_g  # Update the actual cost
                    h_maliyet = self._heuristic(komsu, hedef)  # Compute the heuristic cost
                    maliyet_f[komsu] = yeni_maliyet_g + h_maliyet  # Update the total estimated cost

                    index += 1  # Increment index for uniqueness
                    heapq.heappush(pq, (maliyet_f[komsu], yeni_maliyet_g, index, komsu, yol + [komsu])) # Add the neighbor to the priority queue

        return None  # Return None if no path is found


# Example usage
if __name__ == "__main__":
    metro = MetroAgi()
    
    # Stations and lines
    # Red Line
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Blue Line
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Orange Line
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Adding connections between stations
    # Red Line connections
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Blue Line connections
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Orange Line connections
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Transfer connections (same station, different lines)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Test scenarios
    print("\n=== Test Senaryoları ===")
    
    # Scenario 1: AŞTİ to OSB
    print("\n1. AŞTİ'den OSB'ye:")
    rota = metro.en_az_aktarma_bul("M1", "K4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Scenario 2: Batıkent to Keçiören
    print("\n2. Batıkent'ten Keçiören'e:")
    rota = metro.en_az_aktarma_bul("T1", "T4")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
    
    # Scenario 3: Keçiören to AŞTİ
    print("\n3. Keçiören'den AŞTİ'ye:")
    rota = metro.en_az_aktarma_bul("T4", "M1")
    if rota:
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota)) 