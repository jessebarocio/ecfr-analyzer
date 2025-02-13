declare type Agency = {
  id: number;
  name: string;
  short_name: string;
  parent_id: number | null;
  total_word_count: number;
  burden_category: string;
  children: Agency[];
};
