import { createContext, useCallback, useContext, useState, type ReactNode } from 'react';
import { createPortal } from 'react-dom';

type ModalContent = {
  title?: string;
  body: ReactNode;
};

type ModalContextValue = {
  open: (content: ModalContent) => void;
  close: () => void;
};

const ModalContext = createContext<ModalContextValue | null>(null);

export function ModalProvider({ children }: { children: ReactNode }) {
  const [content, setContent] = useState<ModalContent | null>(null);
  const open = useCallback((c: ModalContent) => setContent(c), []);
  const close = useCallback(() => setContent(null), []);

  return (
    <ModalContext.Provider value={{ open, close }}>
      {children}
      {content &&
        createPortal(
          <div className="modal_backdrop" onClick={close}>
            <div className="modal_window" onClick={e => e.stopPropagation()}>
              <div className="modal_body">{content.body}</div>
              <button onClick={close}>Close</button>
            </div>
          </div>,
          document.body
        )}
    </ModalContext.Provider>
  );
}

export default function Modal() {
  const ctx = useContext(ModalContext);
  if (!ctx) throw new Error('useModal must be used inside <ModalProvider>');
  return ctx;
}
