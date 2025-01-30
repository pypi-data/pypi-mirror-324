import asyncio
from datetime import datetime

from worker_automate_hub.models.dto.rpa_historico_request_dto import (
    RpaHistoricoStatusEnum,
    RpaRetornoProcessoDTO,
    RpaTagDTO,
    RpaTagEnum,
)
from worker_automate_hub.models.dto.rpa_processo_entrada_dto import (
    RpaProcessoEntradaDTO,
)
from rich.console import Console
import re
from pywinauto.keyboard import send_keys
from worker_automate_hub.utils.util import login_emsys
import warnings
from pywinauto.application import Application
from worker_automate_hub.api.client import get_config_by_name
from worker_automate_hub.utils.util import (
    kill_process,
    set_variable,
    type_text_into_field,
    worker_sleep,
)
from pywinauto_recorder.player import set_combobox

from datetime import timedelta
import pyautogui
from worker_automate_hub.utils.logger import logger
from worker_automate_hub.utils.utils_nfe_entrada import EMSys

emsys = EMSys()

console = Console()
pyautogui.PAUSE = 0.5
pyautogui.FAILSAFE = False


async def set_tipo_pagamento_combobox(app: Application, window_title: str):
    try:
        app = Application(backend="uia").connect(process=app.process)
        main_window = app.top_window()
        main_window = main_window.child_window(title="Conhecimento de Frete", found_index=0)
        janelaPagamento = main_window.child_window(title='tsPagamento', found_index=0)
        janelaPagamento.ComboBox.select("BANCO DO BRASIL BOLETO")
        
    except Exception as e:
        console.print(f"Erro ao conectar a janela {window_title}")
        raise Exception(f"Erro ao conectar a janela: {e}")

def calcular_vencimento(data_emissao_str):
    data_emissao = datetime.strptime(data_emissao_str, "%d/%m/%Y")

    if 23 <= data_emissao.day or data_emissao.day <= 8:
        faturamento = datetime(data_emissao.year, data_emissao.month, 9)
        if data_emissao.day >= 23:
            faturamento = faturamento + timedelta(days=31)
            faturamento = faturamento.replace(day=9)
    else:
        faturamento = datetime(data_emissao.year, data_emissao.month, 23)
    if faturamento.weekday() == 5: 
        faturamento -= timedelta(days=1)
    elif faturamento.weekday() == 6: 
        faturamento -= timedelta(days=2)

    vencimento = faturamento + timedelta(days=15)

    if vencimento.weekday() == 5: 
        vencimento -= timedelta(days=1)
    elif vencimento.weekday() == 6: 
        vencimento -= timedelta(days=2)
    return vencimento.strftime("%d/%m/%Y")


async def despesas_cte(task: RpaProcessoEntradaDTO):
    try:
        config = await get_config_by_name("login_emsys")
        console.print(task)
        console.print(config)

        multiplicador_timeout = int(float(task.sistemas[0].timeout))
        set_variable("timeout_multiplicador", multiplicador_timeout)

        await kill_process("EMSys")
        app = Application(backend="win32").start("C:\\Rezende\\EMSys3\\EMSys3.exe")
        warnings.filterwarnings(
            "ignore",
            category=UserWarning,
            message="32-bit application should be automated using 32-bit Python",
        )

        console.print("\nEMSys iniciando...", style="bold green")
        await worker_sleep(5)

        return_login = await login_emsys(config.conConfiguracao, app, task)
        if return_login.sucesso:
            type_text_into_field(
                "Conhecimento de Frete", app["TFrmMenuPrincipal"]["Edit"], True, "50"
            )
            pyautogui.press("enter")
            await worker_sleep(1)
            pyautogui.press("enter")
            await worker_sleep(5)

            console.print(
                "\nPesquisa: 'Conhecimento de Frete' realizada com sucesso",
                style="bold green",
            )
            await worker_sleep(6)

            console.print("conhecimento frete window")
            type_text_into_field(
                task.configEntrada.get("numeroCte"),
                app["TFrmConhecimentoNotaNew"]["Edit26"],
                False,
                "0",
            )
            await worker_sleep(2)

            type_text_into_field(
                task.configEntrada.get("serieCte"),
                app["TFrmConhecimentoNotaNew"]["Edit24"],
                False,
                "0",
            )
            await worker_sleep(2)

            send_keys("{TAB 2}{ENTER}" + task.configEntrada.get("nomeEmitente").replace(' ', '{SPACE}') + "{ENTER}")
            await emsys.verify_warning_and_error("Pesquisa", "&Cancelar")
            await worker_sleep(2)

            app["TFrmConhecimentoNotaNew"]["Edit21"].set_focus()
            app["TFrmConhecimentoNotaNew"]["Edit21"].set_focus()
            send_keys(task.configEntrada.get("dataEmissao").replace("/",""))

            await worker_sleep(2)

            if app["TFrmConhecimentoNotaNew"]["Edit9"].window_text() == '':
                type_text_into_field(
                    task.configEntrada.get("cnpjEmitente"),
                    app["TFrmConhecimentoNotaNew"]["Edit9"],
                    False,
                    "0",
                )
                await worker_sleep(2)

            data_entrada = datetime.now().strftime("%d/%m/%Y")
            app["TFrmConhecimentoNotaNew"]["Edit20"].set_focus()
            app["TFrmConhecimentoNotaNew"]["Edit20"].set_focus()
            app["TFrmConhecimentoNotaNew"]["Edit20"].type_keys(data_entrada.replace("/",""))
            await worker_sleep(2)

            app["TFrmConhecimentoNotaNew"]["ComboBox4"].select(2)
            await worker_sleep(2)
            app["TFrmConhecimentoNotaNew"]["ComboBox3"].select(1)
            await worker_sleep(2)
            app["TFrmConhecimentoNotaNew"]["ComboBox5"].select(2)
            await worker_sleep(2)
            app["TFrmConhecimentoNotaNew"]["ComboBox2"].select("9 - Outros")
            
            await emsys.verify_warning_and_error("Pesquisa", "&Cancelar")
            type_text_into_field(
                task.configEntrada.get("chaveCte"),
                app["TFrmConhecimentoNotaNew"]["Edit10"],
                False,
                "0",
            )

            nomeEmitente = task.configEntrada.get("nomeEmitente").upper()
            listaEmitentes01 = ("Reiter", "COL")
            listaEmitentes02 = (
                "Elton",
                "Gotardo",
                "Leandro Xavier",
                "TVF",
                "Pizzolatto",
                "Arco",
                "Dalçoquio",
                "Borges",
                "Delgado",
            )
            tipo_despesa = "83"
            
            is_reiter_or_col = False

            for emitente in listaEmitentes01:
                emitente = emitente.upper()
                if emitente in nomeEmitente:
                    tipo_despesa = "358"
                    is_reiter_or_col = True
                    break

            for emitente in listaEmitentes02:
                emitente = emitente.upper()
                if emitente in nomeEmitente:
                    tipo_despesa = "359"
                    break

            type_text_into_field(
                tipo_despesa, app["TFrmConhecimentoNotaNew"]["Edit4"], False, "3"
            )
            await worker_sleep(2)
            
            send_keys("{TAB 3}{DOWN}{ENTER}")
            await worker_sleep(3)
            
            type_text_into_field(
                task.configEntrada.get("valorFrete"),
                app["TFrmConhecimentoNotaNew"]["Edit21"],
                False,
                "0",
            )
            await worker_sleep(2)
            
            type_text_into_field(
                task.configEntrada.get("valorFrete"),
                app["TFrmConhecimentoNotaNew"]["Edit15"],
                False,
                "0",
            )
            await worker_sleep(2)
            
            send_keys("{TAB 11}{DOWN}{ENTER}")
            await worker_sleep(2)
            
            
            pyautogui.click(x=1293, y=537)
            await worker_sleep(2)
            
            await set_tipo_pagamento_combobox(app, "Conhecimento de Frete")
            await worker_sleep(2)
            
            dataVencimento = calcular_vencimento(task.configEntrada.get("dataVencimento"))

            send_keys("{TAB}" + dataVencimento)
            await worker_sleep(2)
            
            pyautogui.click(x=1081, y=404)
            await worker_sleep(2)
            
            pyautogui.click(x=1261, y=402)
            await worker_sleep(2)

            if is_reiter_or_col:
                await worker_sleep(10)
                console.print("Aguardando informações de rateio", style="bold yellow")
            else:
                type_text_into_field("100", app["TFrmConhecimentoNotaNew"]["Edit5"], False, "0")
                await worker_sleep(2)
                
                codigo_empresa = int(task.configEntrada.get("codigoEmpresa")) + 1000
                codigo_empresa = str(codigo_empresa)
                type_text_into_field(
                    codigo_empresa, app["TFrmConhecimentoNotaNew"]["Edit4"], False, "0"
                )
                await worker_sleep(2)
                
                pyautogui.click(x=1257, y=617)
                await worker_sleep(2)
                
                await emsys.verify_warning_and_error("Informação", "&Ok")
            
            await worker_sleep(2)
            pyautogui.click(x=584, y=323)
            await worker_sleep(2)
            
            try:
                app = Application().connect(title="Information")
                main_window = app["Information"]
                await worker_sleep(7)
                all_controls_from_error = main_window.children()
                capturar_proxima_mensagem = True
                console.print("Obtendo mensagem de erro mapeada...\n")

                for control in all_controls_from_error:
                    control_text = control.window_text()
                    console.print(control_text)

                    if "frete lançado" in control_text:
                        return RpaRetornoProcessoDTO(
                        sucesso=False,
                        retorno=f"Erro: {control_text}... \n",
                    
                        status=RpaHistoricoStatusEnum.Descartado, tags=[RpaTagDTO(descricao=RpaTagEnum.Negocio)]
                    )
            except:
                await worker_sleep(2)
                return RpaRetornoProcessoDTO(
                    sucesso=True,
                    retorno="Nota Lançada com sucesso!",
                    status=RpaHistoricoStatusEnum.Sucesso,
                )
        else:
            logger.info(f"\nError Message: {return_login.retorno}")
            console.print(f"\nError Message: {return_login.retorno}", style="bold red")
            return RpaRetornoProcessoDTO(
                sucesso=False,
                retorno=f"Erro ao efetuar login no EMsys, erro {error}",
                status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
            )

    except Exception as error:
        console.print(f"Erro ao executar a função rror: {error}")
        return RpaRetornoProcessoDTO(
            sucesso=False,
            retorno=f"Erro ao lançar nota, erro {error}",
            status=RpaHistoricoStatusEnum.Falha, tags=[RpaTagDTO(descricao=RpaTagEnum.Tecnico)]
        )
