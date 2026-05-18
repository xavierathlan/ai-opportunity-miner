from agents.opportunity_agent import OpportunityAgent

agent = OpportunityAgent()

tests = [

    "Pequenos mercados não conseguem competir com grandes redes.",

    "Muitas pessoas esquecem alimentos vencendo na geladeira.",

    "Farmácias pequenas possuem pouca presença digital.",

    "Clínicas locais têm dificuldade para conseguir novos clientes."
]

for test in tests:

    print("\n============================")
    print(f"ENTRADA:\n{test}")

    result = agent.analyze(test)

    print("\nRESPOSTA DA IA:\n")
    print(result) 