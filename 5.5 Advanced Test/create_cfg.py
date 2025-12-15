import matplotlib.pyplot as plt
import networkx as nx

def draw_cfg():
    G = nx.DiGraph()

    # --- Düğümler (Nodes) ---
    # Kodun mantıksal adımlarını düğüm olarak ekliyoruz
    G.add_node("Start", label="Başlangıç\n(Girdi: Saat, Üye Tipi)", shape="ellipse")
    
    # Zaman Mantığı
    G.add_node("TimeCheck1", label="Saat 06-12\nArasında mı?", shape="diamond")
    G.add_node("Morning", label="Çarpan = 0.8", shape="box")
    G.add_node("TimeCheck2", label="Saat 17-24\nArasında mı?", shape="diamond")
    G.add_node("Evening", label="Çarpan = 1.1", shape="box")
    G.add_node("StandardTime", label="Çarpan = 1.0", shape="box")
    
    # Birleşme Noktası 1
    G.add_node("Merge1", label="Zaman Çarpanı\nBelirlendi", shape="circle")

    # Üyelik Mantığı
    G.add_node("MemCheck1", label="Üye Tipi\nStudent mı?", shape="diamond")
    G.add_node("Student", label="Çarpan = 0.8", shape="box")
    G.add_node("MemCheck2", label="Üye Tipi\nPremium mu?", shape="diamond")
    G.add_node("Premium", label="Çarpan = 1.4", shape="box")
    G.add_node("StandardMem", label="Çarpan = 1.0", shape="box")

    # Bitiş
    G.add_node("End", label="Bitiş\n(Fiyatı Döndür)", shape="ellipse")

    # --- Kenarlar (Edges - Yollar) ---
    edges = [
        ("Start", "TimeCheck1"),
        
        # Zaman Dalları
        ("TimeCheck1", "Morning"),       # True
        ("TimeCheck1", "TimeCheck2"),    # False
        ("TimeCheck2", "Evening"),       # True
        ("TimeCheck2", "StandardTime"),  # False
        
        # Zaman Birleşmesi
        ("Morning", "Merge1"),
        ("Evening", "Merge1"),
        ("StandardTime", "Merge1"),

        # Üyelik Dalları
        ("Merge1", "MemCheck1"),
        ("MemCheck1", "Student"),      # True
        ("MemCheck1", "MemCheck2"),    # False
        ("MemCheck2", "Premium"),      # True
        ("MemCheck2", "StandardMem"),  # False

        # Sonuç
        ("Student", "End"),
        ("Premium", "End"),
        ("StandardMem", "End")
    ]
    G.add_edges_from(edges)

    # --- Çizim Ayarları ---
    pos = {
        "Start": (2, 10),
        "TimeCheck1": (2, 9),
        "Morning": (1, 8), "TimeCheck2": (3, 8),
        "Evening": (2.5, 7), "StandardTime": (3.5, 7),
        "Merge1": (2, 6),
        "MemCheck1": (2, 5),
        "Student": (1, 4), "MemCheck2": (3, 4),
        "Premium": (2.5, 3), "StandardMem": (3.5, 3),
        "End": (2, 1)
    }

    plt.figure(figsize=(10, 12))
    
    # Düğümleri ve Etiketleri Çiz
    # Karar kutuları (Diamond) ve İşlem kutuları (Box) ayrımı görsel olarak yapıldı
    nx.draw(G, pos, with_labels=False, node_size=3000, node_color='lightblue', edge_color='gray', arrows=True)
    
    labels = nx.get_node_attributes(G, 'label')
    nx.draw_networkx_labels(G, pos, labels, font_size=9)

    # True/False Etiketlerini Ekle (Okların üzerine)
    edge_labels = {
        ("TimeCheck1", "Morning"): "Evet", ("TimeCheck1", "TimeCheck2"): "Hayır",
        ("TimeCheck2", "Evening"): "Evet", ("TimeCheck2", "StandardTime"): "Hayır",
        ("MemCheck1", "Student"): "Evet", ("MemCheck1", "MemCheck2"): "Hayır",
        ("MemCheck2", "Premium"): "Evet", ("MemCheck2", "StandardMem"): "Hayır"
    }
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    plt.title("Control Flow Graph: calculate_dynamic_price", fontsize=15)
    plt.savefig("control_flow_graph.png")
    plt.show()

if __name__ == "__main__":
    draw_cfg()