"""
FarmTech Solutions - Gestao de culturas (Python)
Estrutura em vetores (listas paralelas) + menu de opcoes.
"""
import math
from pathlib import Path
def ler_numero(mensagem, inteiro=False, atual=None):
    while True:
        texto=input(mensagem).strip()
        if not texto and atual is not None:return atual
        try:
            valor=int(texto) if inteiro else float(texto.replace(",","."))
            if not math.isfinite(valor) or valor<=0: raise ValueError
            return valor
        except (ValueError,OverflowError): print("Informe um numero positivo e finito"+(" inteiro." if inteiro else "."))
nomes_cultura=[]; areas_m2=[]; areas_ha=[]; qtd_ruas=[]; comprimento_rua=[]; produtos=[]; metodos=[]; dosagens_ml_m=[]
def calcular_area_ha(area_m2): return area_m2/10000
def calcular_area_retangulo_m2(comprimento_m,largura_m): return comprimento_m*largura_m
def calcular_volume_total_litros(dosagem_ml_m,comprimento_m,qtd_ruas_cultura): return dosagem_ml_m*comprimento_m*qtd_ruas_cultura/1000
def buscar_indice_por_nome(nome):
    nome=nome.strip().lower()
    for i,cultura in enumerate(nomes_cultura):
        if cultura.lower()==nome:return i
    return -1
def entrada_dados():
    print("\n--- Entrada de dados de uma nova cultura ---"); nome=input("Nome da cultura: ").strip()
    if not nome: print("Nome da cultura obrigatorio."); return
    comprimento_terreno=ler_numero("Comprimento do terreno (m): "); largura_terreno=ler_numero("Largura do terreno (m): ")
    area_m2=calcular_area_retangulo_m2(comprimento_terreno,largura_terreno); area_ha=calcular_area_ha(area_m2)
    ruas=ler_numero("Quantidade de ruas: ",inteiro=True); comprimento=ler_numero("Comprimento de cada rua (m): ")
    produto=input("Produto/insumo aplicado: "); metodo=input("Metodo de aplicacao: "); dosagem=ler_numero("Dosagem (ml por metro de rua): ")
    if not math.isfinite(area_m2) or not math.isfinite(calcular_volume_total_litros(dosagem,comprimento,ruas)): print("Valores muito grandes para calcular area ou volume."); return
    nomes_cultura.append(nome); areas_m2.append(area_m2); areas_ha.append(area_ha); qtd_ruas.append(ruas); comprimento_rua.append(comprimento); produtos.append(produto); metodos.append(metodo); dosagens_ml_m.append(dosagem)
    print(f"\nCultura '{nome}' cadastrada com sucesso!")
def saida_dados():
    print("\n--- Dados cadastrados ---")
    if not nomes_cultura: print("Nenhuma cultura cadastrada ainda."); return
    for i in range(len(nomes_cultura)):
        volume_total=calcular_volume_total_litros(dosagens_ml_m[i],comprimento_rua[i],qtd_ruas[i])
        print(f"\n[{i}] {nomes_cultura[i]}"); print(f"    Area: {areas_m2[i]} m2 ({areas_ha[i]:.2f} ha)"); print(f"    Ruas: {qtd_ruas[i]} x {comprimento_rua[i]} m"); print(f"    Insumo: {produtos[i]} ({metodos[i]})"); print(f"    Dosagem: {dosagens_ml_m[i]} ml/m -> Total: {volume_total:.2f} L")
def atualizar_dados():
    saida_dados()
    if not nomes_cultura:return
    try:
        indice=int(input("\nDigite o indice da cultura a atualizar: "))
        if indice<0 or indice>=len(nomes_cultura): print("Indice invalido."); return
    except ValueError: print("Entrada invalida."); return
    print(f"Atualizando '{nomes_cultura[indice]}'. Deixe em branco para manter o valor atual.")
    ruas=ler_numero(f"Nova quantidade de ruas ({qtd_ruas[indice]}): ",inteiro=True,atual=qtd_ruas[indice]); comprimento=ler_numero(f"Novo comprimento de rua em m ({comprimento_rua[indice]}): ",atual=comprimento_rua[indice]); dosagem=ler_numero(f"Nova dosagem ml/m ({dosagens_ml_m[indice]}): ",atual=dosagens_ml_m[indice])
    if not math.isfinite(calcular_volume_total_litros(dosagem,comprimento,ruas)): print("Valores muito grandes. Registro mantido."); return
    qtd_ruas[indice],comprimento_rua[indice],dosagens_ml_m[indice]=ruas,comprimento,dosagem; print("Dados atualizados com sucesso!")
def deletar_dados():
    saida_dados()
    if not nomes_cultura:return
    try:
        indice=int(input("\nDigite o indice da cultura a deletar: "))
        if indice<0 or indice>=len(nomes_cultura): print("Indice invalido."); return
    except ValueError: print("Entrada invalida."); return
    nome_removido=nomes_cultura[indice]
    for lista in (nomes_cultura,areas_m2,areas_ha,qtd_ruas,comprimento_rua,produtos,metodos,dosagens_ml_m): del lista[indice]
    print(f"Cultura '{nome_removido}' removida com sucesso!")
def exportar_csv(caminho=None):
    import csv
    if caminho is None:caminho=Path(__file__).resolve().with_name("culturas_manejo.csv")
    with open(caminho,mode="w",newline="",encoding="utf-8") as arquivo:
        escritor=csv.writer(arquivo); escritor.writerow(["cultura","area_m2","area_ha","qtd_ruas","comprimento_rua_m","produto","metodo_aplicacao","dosagem_ml_por_metro","volume_total_L"])
        for i in range(len(nomes_cultura)):
            volume_total=calcular_volume_total_litros(dosagens_ml_m[i],comprimento_rua[i],qtd_ruas[i]); escritor.writerow([nomes_cultura[i],areas_m2[i],round(areas_ha[i],2),qtd_ruas[i],comprimento_rua[i],produtos[i],metodos[i],dosagens_ml_m[i],round(volume_total,2)])
    print(f"\nDados exportados para '{caminho}' com sucesso!")
def menu_principal():
    while True:
        print("\n===== FarmTech Solutions ====="); print("1 - Entrada de dados (cadastrar cultura)"); print("2 - Saida de dados (listar culturas)"); print("3 - Atualizar dados"); print("4 - Deletar dados"); print("5 - Exportar para CSV"); print("6 - Sair do programa")
        opcao=input("Escolha uma opcao: ")
        if opcao=="1":entrada_dados()
        elif opcao=="2":saida_dados()
        elif opcao=="3":atualizar_dados()
        elif opcao=="4":deletar_dados()
        elif opcao=="5":exportar_csv()
        elif opcao=="6": print("Encerrando o programa. Ate mais!"); break
        else: print("Opcao invalida, tente novamente.")
if __name__=="__main__":menu_principal()
