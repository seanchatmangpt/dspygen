---
to: frontend/app/<%= name %>/layout.tsx
---
export default function Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <>
      {children}
    </>
  );
}