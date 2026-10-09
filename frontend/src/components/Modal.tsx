import { createContext, useCallback, useContext, useState, type ReactNode } from 'react';

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

      {content && (
        <div className="modal_body">
          {content.body}
        </div>
      )}
    </ModalContext.Provider>
  );
}

export default function Modal() {
  const ctx = useContext(ModalContext);
  if (!ctx) throw new Error('useModal must be used inside <ModalProvider>');
  return ctx;
}
