import fs from "node:fs/promises";

import {
  Document,
  MetadataMode,
  NodeWithScore,
  VectorStoreIndex,
  Ollama,
  Settings,
} from "llamaindex";

const ollama = new Ollama({ model: "llama2", temperature: 0.75 });

Settings.llm = ollama;
Settings.embedModel = ollama;

async function main() {
  // Load essay from abramov.txt in Node
  const essay = await fs.readFile("node_modules/llamaindex/examples/abramov.txt", "utf-8");

  // Create Document object with essay
  const document = new Document({ text: essay, id_: 'essay' });

  // Split text and create embeddings. Store them in a VectorStoreIndex
  const index = await VectorStoreIndex.fromDocuments([document]);

  // Query the index
  const queryEngine = index.asQueryEngine();
  const { response, sourceNodes } = await queryEngine.query({
    query: "What is the meaning of life?",
  });

  // Output response with sources
  console.log(response);

  if (sourceNodes) {
    sourceNodes.forEach((source: NodeWithScore, index: number) => {
      console.log(
        `\n${index}: Score: ${source.score} - ${source.node.getContent(MetadataMode.NONE).substring(0, 50)}...\n`,
      );
    });
  }
}

main().catch(console.error);
