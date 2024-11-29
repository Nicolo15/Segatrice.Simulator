import asyncio
import logging
from asyncua import ua, Server

_logger = logging.getLogger(__name__)


async def main():
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://0.0.0.0:48421/freeopcua/server/")
    server.set_server_name("Segatrice OPC UA Server")

    # Set all possible endpoint policies for clients to connect through
    server.set_security_policy(
        [
            ua.SecurityPolicyType.NoSecurity,
            ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
            ua.SecurityPolicyType.Basic256Sha256_Sign,
        ]
    )

    # Setup our own namespace
    uri = "http://examples.freeopcua.github.io"
    idx = await server.register_namespace(uri)

    # Creare un oggetto Segatrice con le variabili richieste
    segatrice = await server.nodes.objects.add_object(idx, "Segatrice")

    # Stato macchina (int, scrivibile)
    stato_macchina = await segatrice.add_variable(idx, "StatoMacchina", 0)
    await stato_macchina.set_writable()

    # Velocità di taglio (int, scrivibile)
    velocita_taglio = await segatrice.add_variable(idx, "VelocitaTaglio", 0)
    await velocita_taglio.set_writable()

    # Conteggio pezzi tagliati (int, scrivibile)
    conteggio_pezzi = await segatrice.add_variable(idx, "ConteggioPezziTagliati", 0)
    await conteggio_pezzi.set_writable()

    # Consumo energetico (float, scrivibile)
    consumo_energetico = await segatrice.add_variable(idx, "ConsumoEnergetico", 0.0)
    await consumo_energetico.set_writable()

    # Avvio del server
    async with server:
        print("Server OPC UA in esecuzione. Endpoint:", server.endpoint)
        print("Namespace URI:", uri)

        while True:
            await asyncio.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
