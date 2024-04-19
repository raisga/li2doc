import fs from "node:fs/promises";
import {
  Document,
  MetadataMode,
  NodeWithScore,
  VectorStoreIndex,
  storageContextFromDefaults,
  HuggingFaceEmbedding,
  Settings
} from "llamaindex";
import { v4 as uuidv4 } from 'uuid';
import dotenv from "dotenv";

dotenv.config()

Settings.llm = HuggingFaceEmbedding.

async function main() {
  // Load essay from abramov.txt in Node
  const abramovSample = await fs.readFile("node_modules/llamaindex/examples/abramov.txt", "utf-8");
  const pdfSample = await fs.readFile("files/sample.pdf")

  // Create Document object with essay
  const document = new Document({ text: abramovSample, id_: `essay_${uuidv4()}` });

  const storageContext = await storageContextFromDefaults({
    persistDir: "./storage",
  });

  // Split text and create embeddings. Store them in a VectorStoreIndex
  const index = await VectorStoreIndex.fromDocuments([document], { storageContext });

  // Query the index
  const queryEngine = index.asQueryEngine();
  const { response, sourceNodes } = await queryEngine.query({
    query: "What is the meaning of life?",
  });

  // Output response
  console.log(response.toString());

  const secondStorageContext = await storageContextFromDefaults({
    persistDir: "./storage",
  });
  const loadedIndex = await VectorStoreIndex.init({
    storageContext: secondStorageContext,
  });
  const loadedQueryEngine = loadedIndex.asQueryEngine();
  const loadedResponse = await loadedQueryEngine.query({
    query: "What did the author do growing up?",
  });
  console.log(loadedResponse.toString());

  if (sourceNodes) {
    sourceNodes.forEach((source: NodeWithScore, index: number) => {
      console.log(
        `\n${index}: Score: ${source.score} - ${source.node.getContent(MetadataMode.NONE).substring(0, 50)}...\n`,
      );
    });
  }
}

main().catch(console.error);
