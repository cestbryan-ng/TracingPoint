from numpy import *
import matplotlib.pyplot as plt
import tkinter.messagebox as msgbox
import customtkinter as CTk
import re

class MonApp(CTk.CTk):
    def __init__(self):
        super().__init__()
        self.config_interface()
        self.config_polices()
        self.create_interface()
        self.functions_history = []
        
    def config_interface(self):
        self.geometry("800x650")
        self.title("Tracing Point - Traceur de Fonctions")
        self.resizable(True, True)
        CTk.set_appearance_mode("dark")
        CTk.set_default_color_theme("blue")
        
    def config_polices(self):
        self.fonts = {
            'title': CTk.CTkFont(family="Helvetica", size=36, weight="bold"),
            'subtitle': CTk.CTkFont(family="Helvetica", size=14, weight="normal"),
            'button': CTk.CTkFont(family="Helvetica", size=14, weight="bold"),
            'entry': CTk.CTkFont(family="Consolas", size=16),
            'label': CTk.CTkFont(family="Helvetica", size=12, weight="normal")
        }
        
    def create_interface(self):
        self.main_frame = CTk.CTkFrame(
            self, 
            width=760, 
            height=560, 
            corner_radius=20,
            fg_color=("gray85", "gray20")
        )
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        self.titre = CTk.CTkLabel(
            self.main_frame,
            text="TRACING POINT",
            font=self.fonts['title'],
            text_color=("#1f538d", "#4a9eff")
        )
        self.titre.pack(pady=(20, 10))

        self.soustitre = CTk.CTkLabel(
            self.main_frame,
            text="Tracez vos fonctions mathématiques avec cette app",
            font=self.fonts['subtitle'],
            text_color=("gray60", "gray70")
        )
        self.soustitre.pack(pady=(0, 20))
        
        self.input_frame = CTk.CTkFrame(self.main_frame, fg_color="transparent")
        self.input_frame.pack(pady=20, padx=40, fill="x")
        
        self.texte_fonction = CTk.CTkLabel(
            self.input_frame,
            text="Fonction f(x) =",
            font=self.fonts['label'],
            anchor="w"
        )
        self.texte_fonction.pack(anchor="w", pady=(0, 5))
        
        self.entree_fonction = CTk.CTkEntry(
            self.input_frame,
            width=600,
            height=50,
            font=self.fonts['entry'],
            placeholder_text="Exemples: 2x+4, sin(x)**4, sqrt(x), x**3-2x+1",
            corner_radius=15,
            border_width=2
        )
        self.entree_fonction.pack(pady=10, fill="x")
        self.entree_fonction.bind("<Return>", lambda e: self.tracer())
        
        self.params_frame = CTk.CTkFrame(self.main_frame)
        self.params_frame.pack(pady=20, padx=40, fill="both", expand=True)
        
        self.titre_params = CTk.CTkLabel(
            self.params_frame,
            text="Paramètres de tracé",
            font=self.fonts['button']
        )
        self.titre_params.pack(pady=(10, 5))
        
        self.frame_axes = CTk.CTkFrame(self.params_frame, fg_color="transparent")
        self.frame_axes.pack(pady=10, padx=20, fill="both", expand=True)

        self.x_frame = CTk.CTkFrame(self.frame_axes, fg_color="transparent")
        self.x_frame.pack(side="left", padx=10, fill="both", expand=True)
        
        CTk.CTkLabel(self.x_frame, text="Plage X:", font=self.fonts['label']).pack()
        self.x_min = CTk.CTkSlider(self.x_frame, from_=0, to=-500, number_of_steps=100)
        self.x_min.set(-100)
        self.x_min.pack(pady=2)
        CTk.CTkLabel(self.x_frame, text="Min", font=self.fonts['label']).pack()
        
        self.x_max = CTk.CTkSlider(self.x_frame, from_=0, to=500, number_of_steps=100)
        self.x_max.set(100)
        self.x_max.pack(pady=2)
        CTk.CTkLabel(self.x_frame, text="Max", font=self.fonts['label']).pack()
        
        self.frame_boutons = CTk.CTkFrame(self.main_frame, fg_color="transparent")
        self.frame_boutons.pack(pady=30)

        self.bouton_tracer = CTk.CTkButton(
            self.frame_boutons,
            text="Tracer la fonction",
            font=self.fonts['button'],
            width=200,
            height=50,
            corner_radius=25,
            command=self.tracer,
            fg_color="#14943e",
            hover_color=("#14a085", "#12866f")
        )
        self.bouton_tracer.pack(side="left", padx=10)
        
        self.bouton_effacer = CTk.CTkButton(
            self.frame_boutons,
            text="Effacer",
            font=self.fonts['button'],
            width=150,
            height=50,
            corner_radius=25,
            command=self.effacer,
            fg_color=("#d4613a", "#d4613a"),
            hover_color=("#b8441f", "#b8441f")
        )
        self.bouton_effacer.pack(side="left", padx=10)

        self.bouton_quitter = CTk.CTkButton(
            self.frame_boutons,
            text="Quitter",
            font=self.fonts['button'],
            width=150,
            height=50,
            corner_radius=25,
            command=self.fermer,
            fg_color=("#c41e3a", "#c41e3a"),
            hover_color=("#a01729", "#a01729")
        )
        self.bouton_quitter.pack(side="left", padx=10)
        
    def preparation_fonction(self, fonction):
        nouvelle_fonction = re.sub(r'([0-9])x', r'\1*x', fonction)
        nouvelle_fonction = re.sub(r'x([0-9])', r'x*\1', nouvelle_fonction) 
        nouvelle_fonction = re.sub(r'\)([0-9])', r')*\1', nouvelle_fonction)
        nouvelle_fonction = re.sub(r'([0-9])\(', r'\1*(', nouvelle_fonction)
        return nouvelle_fonction
            
    def tracer(self):
        fonction = self.entree_fonction.get().strip()
        x_min = self.x_min.get()
        x_max = self.x_max.get()
        
        if not fonction:
            msgbox.showwarning("Attention", "Veuillez entrer une fonction.")
            return
        
        if x_min >= x_max:
            msgbox.showwarning("Attention", "x_min est plus grand ou égale que x_max.")
            return
            
        try:
            nouvelle_fonction = self.preparation_fonction(fonction)
            print(nouvelle_fonction)
            
            X = linspace(x_min, x_max, 20000)
            Y = []
            
            points_fonction = 0
            for x in X:
                try :
                    y_val = eval(nouvelle_fonction, globals(), {"x": x})
                    if isinf(y_val) or isnan(y_val):
                        Y.append(nan)
                    else : 
                        Y.append(y_val)
                        points_fonction += 1    
                except :
                    Y.append(nan)
                    
            if points_fonction == 0:
                raise ValueError("Aucun point valide trouvé")
                
            Y = array(Y)

            segments = []
            segment_x = []
            segment_y = []

            for i in range(len(X)):
                if not isnan(Y[i]):
                    if len(segment_y) > 0:
                        diff = abs(Y[i] - segment_y[-1])
                        dx = X[i] - segment_x[-1]
                        pente = diff / dx if dx > 0 else 0

                        if pente > 1000:
                            if len(segment_x) > 1:
                                segments.append((list(segment_x), list(segment_y)))
                            segment_x = [X[i]]
                            segment_y = [Y[i]]
                        else:
                            segment_x.append(X[i])
                            segment_y.append(Y[i])
                    else:
                        segment_x.append(X[i])
                        segment_y.append(Y[i])
                else:
                    if len(segment_x) > 1:
                        segments.append((list(segment_x), list(segment_y)))
                    segment_x = []
                    segment_y = []

            if len(segment_x) > 1:
                segments.append((list(segment_x), list(segment_y)))

            plt.figure(figsize=(12, 8))

            if len(segments) > 0:
                for i, (xs, ys) in enumerate(segments):
                    if i == 0:
                        plt.plot(xs, ys, linewidth=2.5, label=f'f(x) = {fonction}', color='#1f77b4')
                    else:
                        plt.plot(xs, ys, linewidth=2.5, color='#1f77b4')
            else:
                plt.plot(X, Y, linewidth=2.5, label=f'f(x) = {fonction}', color='#1f77b4')
            plt.xlim(-10, 10)
            plt.ylim(-7, 7)
            plt.grid(True, alpha=0.3, linestyle='--')
            plt.axhline(y=0, color='k', linewidth=0.8, alpha=0.7)
            plt.axvline(x=0, color='k', linewidth=0.8, alpha=0.7)
            plt.xlabel("x", fontsize=14, fontweight='bold')
            plt.ylabel("f(x)", fontsize=14, fontweight='bold')
            plt.title(f"Fonction f(x) = {fonction}", fontsize=16, fontweight='bold', pad=20)
            plt.legend(fontsize=12, framealpha=0.9)
            plt.tight_layout()
            
            if fonction not in self.functions_history:
                self.functions_history.append(fonction)
                
            plt.show()
            
        except Exception as e:
            error_msg = (
                f"Erreur lors du tracé de la fonction:\n\n"
                f"Fonction entrée: {fonction}\n"
                f"Erreur: {str(e)}\n\n"
                f"Conseils:\n"
                f"Utilisez 'x' comme variable\n"
                f"Vérifiez la syntaxe des fonctions mathématiques\n"
                f"Évitez les divisions par zéro"
            )
            msgbox.showerror("Erreur de tracé", error_msg)
            
    def effacer(self):
        plt.close('all')
        
    def fermer(self):
        plt.close('all')
        self.quit()
        self.destroy()

def main():
    app = MonApp()
    app.mainloop()

if __name__ == "__main__":
    main()