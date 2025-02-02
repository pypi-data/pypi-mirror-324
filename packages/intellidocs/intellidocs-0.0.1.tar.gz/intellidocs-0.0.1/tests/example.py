from intellibricks.llms import Synapse

from intellidocs.document_creators import DocumentCreator

llm = Synapse.of("openai/api/gpt-4o")

pptx_creator = DocumentCreator.of("pptx", llm=llm)
pptx = pptx_creator.create("Give me slides about rome")
pptx.save("rome.pptx")
