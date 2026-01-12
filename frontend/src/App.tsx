import { Navigate, Route, Routes } from "react-router-dom";
import NavBar from "./components/NavBar";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import FilesPage from "./pages/FilesPage";
import SearchPage from "./pages/SearchPage";
import { getToken } from "./lib/auth";

const RequireAuth = ({ children }: { children: JSX.Element }) => {
  const token = getToken();
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

const App = () => {
  return (
    <div className="app">
      <NavBar />
      <div className="container">
        <Routes>
          <Route path="/" element={<Navigate to="/files" replace />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route
            path="/files"
            element={
              <RequireAuth>
                <FilesPage />
              </RequireAuth>
            }
          />
          <Route
            path="/search"
            element={
              <RequireAuth>
                <SearchPage />
              </RequireAuth>
            }
          />
          <Route path="*" element={<Navigate to="/files" replace />} />
        </Routes>
      </div>
    </div>
  );
};

export default App;
