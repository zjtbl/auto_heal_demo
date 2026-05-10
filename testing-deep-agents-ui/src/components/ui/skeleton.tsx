import { cn } from "@/lib/utils";
// NOTE  MC8yOmFIVnBZMlhtbkxIbXNaL210cHM2UkdWVlRRPT06Mjk5ZmIyNTk=

function Skeleton({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn("animate-pulse rounded-md bg-muted", className)}
      {...props}
    />
  );
}

export { Skeleton };
// eslint-disable  MS8yOmFIVnBZMlhtbkxIbXNaL210cHM2UkdWVlRRPT06Mjk5ZmIyNTk=
