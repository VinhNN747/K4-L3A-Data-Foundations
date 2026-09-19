# Báo Cáo Cá Nhân — Lab 7: Embedding & Vector Store

**Họ tên:** Nguyễn Ngọc Vĩnh
**Nhóm:** TwoMenSquad
**Ngày:** 19/09/2026

> **Nộp 1 bản / sinh viên.** Phần nhóm (lựa chọn tài liệu, thiết kế chiến lược, bộ câu hỏi đánh giá, demo) nộp chung 1 bản trong `REPORT_NHOM.md`. Chi tiết thang điểm: `docs/SCORING.md`.

**Tổng điểm phần cá nhân: 60** = Khởi động (5) + Hướng tiếp cận (10) + Hoàn thiện code (30) + Dự đoán độ tương tự (5) + Kết quả truy xuất của tôi (10).

---

## 1. Khởi động (Warm-up) — Cá nhân (5 điểm)

### Độ tương tự Cosine (Cosine Similarity) (Bài tập 1.1)

**Độ tương tự cosine cao (High cosine similarity) nghĩa là gì?**
> Là hai vector có hướng gần nhau, tức là chúng biểu diễn các ý nghĩa hoặc nội dung tương tự trong không gian vector.

**Ví dụ có độ tương tự CAO:**
- Câu A: The cat is sitting on the mat.
- Câu B: A feline is resting on the rug.
- Tại sao tương đồng: vì cả hai câu đều mô tả cùng một hành động của một con mèo trên một bề mặt, mặc dù sử dụng từ ngữ khác nhau.

**Ví dụ có độ tương tự THẤP:**
- Câu A: The cat is sitting on the mat.
- Câu B: I like ice cream.
- Tại sao khác: vì hai câu này nói về các chủ đề hoàn toàn khác nhau, không có mối liên hệ về ngữ nghĩa.

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**
> Độ tương tự cosine đo lường hướng của các vector thay vì khoảng cách tuyệt đối, giúp giảm thiểu ảnh hưởng của độ dài vector và tập trung vào nội dung ý nghĩa, điều này quan trọng trong việc so sánh các embeddings văn bản.

**Tại sao độ tương tự cosine (cosine similarity) được ưu tiên hơn khoảng cách Euclid (Euclidean distance) cho text embeddings?**
> Vì độ tương tự cosine đo lường hướng của các vector thay vì khoảng cách tuyệt đối, giúp giảm thiểu ảnh hưởng của độ dài vector và tập trung vào nội dung ý nghĩa, điều này quan trọng trong việc so sánh các embeddings văn bản.

### Bài toán tính toán Chunking (Bài tập 1.2)

**Tài liệu 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> *Trình bày phép tính:*  10,000 / (500 - 50) = 10,000 / 450 ≈ 22.22, làm tròn lên thành 23 chunks.
> *Đáp án:*  23 chunks

**Nếu độ chồng chéo (overlap) tăng lên 100, số lượng chunk thay đổi thế nào? Tại sao muốn độ chồng chéo nhiều hơn?**
> Nếu overlap tăng lên 100, số lượng chunk sẽ giảm vì mỗi chunk mới sẽ bắt đầu sớm hơn, dẫn đến ít chunk hơn. Độ chồng chéo nhiều hơn giúp giữ ngữ cảnh giữa các chunk, cải thiện khả năng truy xuất thông tin liên quan.
---

## 2. Hướng tiếp cận của tôi (My Approach) — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi lập trình (implement) các phần chính trong gói `src`.
> Cách tiếp cận của tôi là sử dụng các lớp và phương thức đã được định nghĩa trong gói `src` để xử lý dữ liệu văn bản. Tôi bắt đầu bằng việc đọc các tài liệu Markdown từ thư mục `data/`, sau đó sử dụng `SentenceChunker` để chia nhỏ nội dung thành các chunk dựa trên câu. Tiếp theo, tôi áp dụng `RecursiveChunker` để đảm bảo rằng các chunk không vượt quá kích thước tối đa và vẫn giữ được ngữ cảnh. Sau khi có các chunk, tôi lưu trữ chúng trong `EmbeddingStore`, nơi tôi tính toán embeddings cho từng chunk và lưu trữ chúng cùng với metadata liên quan. Cuối cùng, tôi triển khai các phương thức tìm kiếm và lọc để truy xuất thông tin một cách hiệu quả, đồng thời đảm bảo rằng các kết quả trả về là chính xác và liên quan đến truy vấn của người dùng.
### Các hàm chia nhỏ (Chunking Functions)

**`SentenceChunker.chunk`** — hướng tiếp cận:
> *Viết 2-3 câu: dùng biểu thức chính quy (regex) gì để phát hiện câu? Xử lý trường hợp ngoại lệ (edge case) nào?*
> Tôi sử dụng biểu thức chính quy để phát hiện các dấu chấm câu kết thúc câu như ".", "!", và "?". Để xử lý các trường hợp ngoại lệ, tôi kiểm tra các trường hợp như dấu chấm trong số thập phân hoặc viết tắt (ví dụ: "Dr.", "e.g.") để tránh chia nhỏ sai. Ngoài ra, tôi cũng đảm bảo rằng các câu không bị cắt ngang bởi các ký tự đặc biệt hoặc khoảng trắng không cần thiết. 
**`RecursiveChunker.chunk` / `_split`** — hướng tiếp cận:
> *Viết 2-3 câu: thuật toán hoạt động thế nào? Base case (trường hợp cơ sở) là gì?*
> Thuật toán hoạt động bằng cách kiểm tra độ dài của chunk hiện tại. Nếu chunk vượt quá kích thước tối đa, nó sẽ được chia nhỏ thành các phần con dựa trên các dấu ngắt câu hoặc từ khóa. Base case là khi chunk đã đủ nhỏ (dưới kích thước tối đa) hoặc không còn cách nào để chia nhỏ mà vẫn giữ nguyên ngữ cảnh, lúc đó thuật toán sẽ dừng lại và trả về chunk hiện tại.
### Lớp EmbeddingStore

**`add_documents` + `search`** — hướng tiếp cận:
> *Viết 2-3 câu: lưu trữ thế nào? Tính độ tương tự ra sao?*
> Tôi lưu trữ các chunk cùng với metadata của chúng trong một cơ sở dữ liệu vector, nơi mỗi chunk được biểu diễn bằng một vector embedding. Khi thực hiện tìm kiếm, tôi tính toán độ tương tự cosine giữa vector embedding của truy vấn và các vector embedding của các chunk trong cơ sở dữ liệu. Kết quả trả về là các chunk có độ tương tự cao nhất với truy vấn, được sắp xếp theo thứ tự giảm dần của độ tương tự.
**`search_with_filter` + `delete_document`** — hướng tiếp cận:
> *Viết 2-3 câu: lọc (filter) trước hay sau? Xóa bằng cách nào?*
> Tôi thực hiện lọc trước khi tính toán độ tương tự để giảm số lượng chunk cần so sánh, giúp tăng hiệu suất tìm kiếm. Việc lọc dựa trên các trường metadata như `audience`, `department`, hoặc `category` để chỉ giữ lại các chunk phù hợp với yêu cầu của truy vấn. Khi xóa một document, tôi xác định các chunk liên quan đến document đó và loại bỏ chúng khỏi cơ sở dữ liệu vector, đồng thời cập nhật các chỉ mục để đảm bảo tính nhất quán của dữ liệu.
### Tác tử KnowledgeBaseAgent

**`answer`** — hướng tiếp cận:
> *Viết 2-3 câu: cấu trúc prompt? Cách đưa ngữ cảnh (inject context) vào thế nào?*
> Tôi cấu trúc prompt bằng cách kết hợp truy vấn của người dùng với các chunk liên quan được tìm thấy từ cơ sở dữ liệu vector. Ngữ cảnh được đưa vào bằng cách chèn các chunk này vào phần đầu của prompt, giúp mô hình hiểu rõ hơn về thông tin liên quan trước khi trả lời. Tôi cũng đảm bảo rằng prompt được định dạng một cách rõ ràng và dễ hiểu để tối ưu hóa khả năng sinh câu trả lời chính xác từ mô hình.
---

## 3. Hoàn thiện code (Core Implementation) — Cá nhân (30 điểm)

Vượt qua bộ kiểm thử là điều kiện tính điểm phần này.

### Kết Quả Kiểm Thử (Test Results)

```
# Dán kết quả (output) của: pytest tests/ -v
============================================== test session starts ===============================================
platform win32 -- Python 3.12.1, pytest-9.1.1, pluggy-1.6.0 -- C:\Users\VinhNN\Desktop\AI_In_Action\K4-L3A-Data-Foundations\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\VinhNN\Desktop\AI_In_Action\K4-L3A-Data-Foundations
plugins: anyio-4.15.1
collected 42 items                                                                                                

tests/test_solution.py::TestProjectStructure::test_root_main_entrypoint_exists PASSED                       [  2%]
tests/test_solution.py::TestProjectStructure::test_src_package_exists PASSED                                [  4%]
tests/test_solution.py::TestClassBasedInterfaces::test_chunker_classes_exist PASSED                         [  7%]
tests/test_solution.py::TestClassBasedInterfaces::test_mock_embedder_exists PASSED                          [  9%]
tests/test_solution.py::TestFixedSizeChunker::test_chunks_respect_size PASSED                               [ 11%]
tests/test_solution.py::TestFixedSizeChunker::test_correct_number_of_chunks_no_overlap PASSED               [ 14%]
tests/test_solution.py::TestFixedSizeChunker::test_empty_text_returns_empty_list PASSED                     [ 16%]
tests/test_solution.py::TestFixedSizeChunker::test_no_overlap_no_shared_content PASSED                      [ 19%]
tests/test_solution.py::TestFixedSizeChunker::test_overlap_creates_shared_content PASSED                    [ 21%]
tests/test_solution.py::TestFixedSizeChunker::test_returns_list PASSED                                      [ 23%]
tests/test_solution.py::TestFixedSizeChunker::test_single_chunk_if_text_shorter PASSED                      [ 26%]
tests/test_solution.py::TestSentenceChunker::test_chunks_are_strings PASSED                                 [ 28%]
tests/test_solution.py::TestSentenceChunker::test_respects_max_sentences PASSED                             [ 30%]
tests/test_solution.py::TestSentenceChunker::test_returns_list PASSED                                       [ 33%]
tests/test_solution.py::TestSentenceChunker::test_single_sentence_max_gives_many_chunks PASSED              [ 35%]
tests/test_solution.py::TestRecursiveChunker::test_chunks_within_size_when_possible PASSED                  [ 38%]
tests/test_solution.py::TestRecursiveChunker::test_empty_separators_falls_back_gracefully PASSED            [ 40%]
tests/test_solution.py::TestRecursiveChunker::test_handles_double_newline_separator PASSED                  [ 42%]
tests/test_solution.py::TestRecursiveChunker::test_returns_list PASSED                                      [ 45%]
tests/test_solution.py::TestEmbeddingStore::test_add_documents_increases_size PASSED                        [ 47%]
tests/test_solution.py::TestEmbeddingStore::test_add_more_increases_further PASSED                          [ 50%]
tests/test_solution.py::TestEmbeddingStore::test_initial_size_is_zero PASSED                                [ 52%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_content_key PASSED                     [ 54%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_have_score_key PASSED                       [ 57%]
tests/test_solution.py::TestEmbeddingStore::test_search_results_sorted_by_score_descending PASSED           [ 59%]
tests/test_solution.py::TestEmbeddingStore::test_search_returns_at_most_top_k PASSED                        [ 61%]
tests/test_solution.py::TestEmbeddingStore::test_search_returns_list PASSED                                 [ 64%]
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_non_empty PASSED                                [ 66%]
tests/test_solution.py::TestKnowledgeBaseAgent::test_answer_returns_string PASSED                           [ 69%]
tests/test_solution.py::TestComputeSimilarity::test_identical_vectors_return_1 PASSED                       [ 71%]
tests/test_solution.py::TestComputeSimilarity::test_opposite_vectors_return_minus_1 PASSED                  [ 73%]
tests/test_solution.py::TestComputeSimilarity::test_orthogonal_vectors_return_0 PASSED                      [ 76%]
tests/test_solution.py::TestComputeSimilarity::test_zero_vector_returns_0 PASSED                            [ 78%]
tests/test_solution.py::TestCompareChunkingStrategies::test_counts_are_positive PASSED                      [ 80%]
tests/test_solution.py::TestCompareChunkingStrategies::test_each_strategy_has_count_and_avg_length PASSED   [ 83%]
tests/test_solution.py::TestCompareChunkingStrategies::test_returns_three_strategies PASSED                 [ 85%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_filter_by_department PASSED                [ 88%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_no_filter_returns_all_candidates PASSED    [ 90%]
tests/test_solution.py::TestEmbeddingStoreSearchWithFilter::test_returns_at_most_top_k PASSED               [ 92%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_reduces_collection_size PASSED        [ 95%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_false_for_nonexistent_doc PASSED [ 97%]
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_true_for_existing_doc PASSED  [100%]

=============================================== 42 passed in 0.36s ===============================================
```

**Số lượng bài test vượt qua (pass):** 42 / 42

---

## 4. Dự đoán độ tương tự (Similarity Predictions) — Cá nhân (5 điểm)

| Cặp | Câu A | Câu B | Dự đoán | Điểm thực tế | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | Sinh viên có thành tích học tập xuất sắc được xét học bổng. | Học bổng được trao cho sinh viên đạt kết quả học tập tốt. | Cao | 0.162000 (thấp) | Không |
| 2 | Hạn nộp hồ sơ học bổng là ngày 30 tháng 9. | Sinh viên phải gửi hồ sơ trước ngày 30 tháng 9. | Cao | 0.129593 (thấp) | Không |
| 3 | Học bổng hỗ trợ chi phí học tập cho sinh viên. | Sinh viên phải hoàn thành nghĩa vụ đóng học phí. | Thấp | 0.007655 (thấp) | Có |
| 4 | Sinh viên được xét học bổng khuyến khích học tập. | Giảng viên đăng ký lịch coi thi cuối kỳ. | Thấp | 0.062359 (thấp) | Có |
| 5 | Ứng viên không được nhận đồng thời hai học bổng. | Ứng viên có thể nhận hai học bổng cùng một lúc. | Cao | 0.009058 (thấp) | Không |

*Cách chạy:* nhúng từng câu bằng backend mặc định `_mock_embed`, sau đó gọi `compute_similarity(vector_a, vector_b)`. Trong bảng này, điểm từ `0.5` trở lên được quy ước là cao; dưới `0.5` là thấp.

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn ý nghĩa?**
> Kết quả bất ngờ nhất là cặp 1: hai câu gần như diễn đạt cùng một ý nhưng chỉ đạt `0.162000`. Nguyên nhân là `_mock_embed` tạo vector xác định từ mã băm của toàn bộ chuỗi chứ không học ngữ nghĩa, nên một thay đổi nhỏ trong cách diễn đạt có thể tạo ra vector hoàn toàn khác. Vì vậy, kết quả này phù hợp để kiểm thử luồng tính toán nhưng không nên dùng để đánh giá khả năng hiểu nghĩa; một mô hình embedding đa ngữ thực sẽ phù hợp hơn cho corpus tiếng Việt.

---

## 5. Kết quả truy xuất của tôi (Competition Results) — Cá nhân (10 điểm)

Chạy **5 câu hỏi đánh giá của nhóm** trên mã nguồn cá nhân của bạn trong gói `src`. **5 câu hỏi này phải trùng với các thành viên cùng nhóm** (xem `REPORT_NHOM.md`).

| # | Câu hỏi (Query) | Top-1 Chunk truy xuất được (tóm tắt) | Điểm Score | Có liên quan không? (Relevant) | Câu trả lời của Agent (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Điều kiện để sinh viên được xét học bổng Data Nest là gì? | Thông tin mở đầu và tiêu đề “Đối tượng sau điều chỉnh” của Data Nest (`uet-data-nest-adjustment-2026-2027#0`). | 0.198321 | Một phần | Nhận diện đúng tài liệu nhưng top-3 không chứa đầy đủ các điều kiện GPA, rèn luyện và hoàn cảnh khó khăn. |
| 2 | Học bổng EVN có giá trị bao nhiêu và có bao nhiêu suất? | Hướng dẫn hồ sơ và thời hạn nộp EVN (`uet-evn-2025-2026#5`). | 0.312087 | Không | Không lấy được chunk “Giá trị và chỉ tiêu”, nên không trả lời được 10.000.000 đồng và 15 suất. |
| 3 | Chương trình Goertek có những mô hình đào tạo nào? | Một phần mô hình Việt Nam của Goertek (`uet-goertek-2027#1`). | 0.260393 | Một phần | Lấy được mô hình đào tạo tại Việt Nam nhưng thiếu mô hình đào tạo tại Trung Quốc. |
| 4 | Sinh viên chương trình CLC CNTT loại Giỏi được nhận học bổng kỳ cuối bao nhiêu? | Danh mục tài liệu tham chiếu của quy định học bổng (`uet-scholarship-regulation-2026#1`). | 0.304166 | Không | Không truy xuất được bảng mức 4.000.000 đồng/sinh viên/tháng. |
| 5 | Hạn đăng ký học bổng The Best of MB Chasing 2026 là khi nào? | Phần mở đầu và thông tin chương trình MB Chasing 2026 (`uet-mb-best-of-chasing-2026#0`). | 0.228019 | Có | Chunk top-1 chứa thông tin chương trình và hạn đăng ký 12h00 ngày 10/08/2026. |

*Thiết lập chạy:* `SentenceChunker(max_sentences_per_chunk=3)`, `_mock_embed`, `top_k=3` và `metadata_filter={"audience": "student"}`. Điểm trong bảng là score của chunk top-1. Vì `_mock_embed` sinh vector từ mã băm thay vì ngữ nghĩa, kết quả này phản ánh một baseline kỹ thuật hơn là chất lượng truy xuất ngữ nghĩa tiếng Việt.

**Bao nhiêu câu hỏi trả về chunk có liên quan trong top-3?** 3 / 5 (1 câu đầy đủ, 2 câu một phần)

**Điều hay nhất tôi học được từ thành viên khác / nhóm khác (qua demo):**
> *Viết 2-3 câu:* > Tôi học được rằng việc lựa chọn chiến lược chunking và thiết kế metadata có thể ảnh hưởng đáng kể đến chất lượng truy xuất. Một số thành viên đã sử dụng các chiến lược chunking khác nhau, như RecursiveChunker với các dấu phân cách thông minh, giúp giữ ngữ cảnh tốt hơn và cải thiện khả năng tìm kiếm. Ngoài ra, việc áp dụng metadata chi tiết hơn cũng giúp lọc kết quả hiệu quả hơn, dẫn đến các chunk liên quan được truy xuất dễ dàng hơn.

---

## Tự Đánh Giá (Phần Cá Nhân)

| Tiêu chí | Điểm tự đánh giá |
|----------|-------------------|
| Khởi động (Warm-up) | 5 / 5 |
| Hướng tiếp cận của tôi (My Approach) | 7 / 10 |
| Hoàn thiện code (Core Implementation — tests) | 20 / 30 |
| Dự đoán độ tương tự (Similarity Predictions) | 4 / 5 |
| Kết quả truy xuất của tôi (Competition Results) | 8 / 10 |
| **Tổng phần cá nhân** | **44 / 60** |
