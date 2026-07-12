import Upload from "./components/Upload";
import Chat from "./components/Chat";
import "./App.css";

function App() {
  return (
    <div className="container">
      <h1>📄 RAG AI Document Chat</h1>

      <Upload />

      <Chat />
    </div>
  );
}

export default App;