export type Contract = {
  id: string;
  title: string;
  client: string;
  status: 'Pending' | 'Approved' | 'Rejected';
};
