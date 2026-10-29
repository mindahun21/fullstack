import { useState, useEffect } from 'react';
import { taskApi, type Task } from './api/tasks';

export function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchTasks = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await taskApi.getAll();
      setTasks(data);
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Could not connect to backend';
      setError(`${msg} (Ensure Django backend is running at http://localhost:8080)`);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800">
      {/* Header */}
      <header className="bg-white border-b border-slate-200">
        <div className="max-w-5xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-lg bg-emerald-600 flex items-center justify-center text-white font-bold text-sm">
              TM
            </div>
            <div>
              <h1 className="font-semibold text-slate-900 text-base leading-tight">
                Task Manager
              </h1>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={fetchTasks}
              className="px-3 py-1.5 text-xs font-medium bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-md transition"
            >
              Refresh
            </button>
            <button
              onClick={() => alert('Ready for task creation implementation!')}
              className="px-3.5 py-1.5 text-xs font-semibold bg-emerald-600 hover:bg-emerald-700 text-white rounded-md transition shadow-xs"
            >
              + Create Task
            </button>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-5xl mx-auto px-4 py-8">
        {error && (
          <div className="mb-6 p-4 rounded-lg bg-amber-50 border border-amber-200 text-amber-800 text-xs">
            <span className="font-semibold">Connection Note:</span> {error}
          </div>
        )}

        <div className="bg-white border border-slate-200 rounded-lg shadow-xs overflow-hidden">
          <div className="px-6 py-4 border-b border-slate-200 flex items-center justify-between">
            <h2 className="text-sm font-semibold text-slate-800">Tasks List</h2>
            <span className="text-xs text-slate-500">{tasks.length} total</span>
          </div>

          {loading ? (
            <div className="py-12 text-center text-sm text-slate-400">Loading tasks...</div>
          ) : tasks.length === 0 ? (
            <div className="py-12 text-center text-sm text-slate-400">
              No tasks found. Click "+ Create Task" to begin.
            </div>
          ) : (
            <div className="divide-y divide-slate-100">
              {tasks.map((t) => (
                <div key={t.id} className="p-4 sm:px-6 flex items-center justify-between hover:bg-slate-50 transition">
                  <div>
                    <h3 className="text-sm font-medium text-slate-900">{t.title}</h3>
                    {t.description && (
                      <p className="text-xs text-slate-500 mt-0.5">{t.description}</p>
                    )}
                  </div>
                  <span className="text-xs px-2.5 py-1 rounded-full font-medium bg-slate-100 text-slate-700">
                    {t.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>

      {/* 
        REFERENCE SNIPPETS FOR CANDIDATE LIVE CODING:
        - Create/Edit Task Modal state:
          const [modalOpen, setModalOpen] = useState(false);
          const [editingTask, setEditingTask] = useState<Task | null>(null);
        - Status values: 'TODO' | 'IN_PROGRESS' | 'DONE'
        - Delete API: await taskApi.delete(id); fetchTasks();
      */}
    </div>
  );
}

export default App;
